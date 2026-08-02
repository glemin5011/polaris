# ADR-011: Deploy Next.js on Vercel as an Authenticated BFF

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS is an authenticated, interactive portfolio application whose invited users work with private workspace content inside the low-sensitivity boundary defined by ADR-021. Static export would force the browser to manage Cognito tokens and would prevent server-side session handling, protected request-time rendering, and a same-origin backend-for-frontend.

FastAPI must remain the only business API and authoritative authorization boundary. The web runtime needs enough server capability to manage authentication and adapt presentation requests without becoming a second application backend.

## Decision

Deploy the Next.js App Router application from `apps/web` through Vercel Git integration and build it with Turborepo.

Use a supported stable Auth.js release with Cognito as its OpenID Connect provider. Pin the exact package version and verify it against the selected Next.js major in CI. Production must not use a beta, release-candidate, or other prerelease authentication package without an explicit architecture and security review. Cognito uses the authorization-code flow and a confidential app client. Auth.js stores the session in an encrypted `Secure`, `HttpOnly`, `SameSite=Lax` JWT cookie; POLARIS does not add a session database.

Disable Cognito self-registration. Production accounts are created by a maintainer invitation through a narrowly privileged AWS operator role using the console or operator CLI, and Cognito-managed TOTP MFA is required. Cognito account recovery uses a verified email address; POLARIS does not build a custom credential or recovery interface. A Cognito account does not grant workspace access by itself: the maintainer grants an explicit membership through FastAPI. Deprovisioning is also a maintainer runbook: remove workspace memberships through FastAPI first, then use the operator role to disable the Cognito account and perform administrative global sign-out. No Vercel or application-runtime role receives Cognito administrative permissions.

The Auth.js server runtime may retain Cognito access and refresh tokens inside the encrypted session representation. Browser JavaScript receives only the minimum user and session display data and never receives either token.

All authenticated browser control-plane requests pass through explicit Next.js BFF adapters under `/api/bff/*`. Auth.js owns `/api/auth/*`. The BFF and server-rendered components use the generated FastAPI client and attach the current Cognito access token to allowlisted `/api/v1/*` requests. They rebuild upstream headers from a positive allowlist; caller-supplied authorization, identity, cookie, host, forwarding, hop-by-hop, and AWS request-context headers are never forwarded. They preserve FastAPI status codes, problem details, concurrency headers, idempotency headers, retry metadata, and correlation identifiers through a response-header allowlist that never relays upstream cookies or hop-by-hop headers.

Cognito access tokens expire after 15 minutes. The Auth.js session and Cognito refresh token expire after eight hours. Refresh-token rotation uses Cognito's maximum retry grace period. Auth.js requires a small custom refresh implementation because automatic provider refresh is not built in.

The deployment does not add a session database, Redis, or a distributed refresh lock. Concurrent refreshes may race across Vercel instances; the grace period permits normal retries, and a failed refresh or unresolved race deletes the local session and requires authentication again. This occasional reauthentication is an accepted simplicity trade-off. Logout deletes the Auth.js cookie, revokes the Cognito refresh token, and redirects through Cognito's logout endpoint.

Production uses one stable HTTPS custom domain, callback URL, logout URL, and Cognito app client. Pull-request previews are protected, receive no production authentication or API secrets, and are not registered as Cognito callbacks. Localhost is the only non-HTTPS callback and uses the development identity path from ADR-010 instead of production Cognito. A separately authenticated staging environment is not part of this deployment.

FastAPI remains the only business API. API Gateway's JWT authorizer validates the forwarded Cognito token's signature, issuer, expiry, app client or audience, and route scopes before Lambda invocation. Lambda Web Adapter conveys the HTTP API v2 authorizer context through its overwritten `x-amzn-request-context` header. FastAPI fails closed unless that context has the expected structure, requires the expected access-token `token_use`, maps Cognito `sub` to the actor, and performs authoritative workspace and domain authorization. The API Lambda resource policy grants API Gateway only from the configured execution ARN, and normal human, runtime, CI, and deployment roles have no direct invocation permission. This IAM rule is part of the trust boundary because authorizer context is not self-authenticating inside Lambda. Next.js may handle login, session state, bearer-token attachment, request-time presentation rendering, and presentation-specific aggregation only.

Auth.js applies its own CSRF protections to `/api/auth/*`. State-changing `/api/bff/*` Route Handlers independently require an application CSRF token and validated `Origin` and `Host` values. Server Actions retain Next.js same-origin `Origin` and `Host` enforcement and bounded request bodies, authenticate the session at entry, and are treated as public endpoints rather than trusted internal calls. All BFF adapters use explicit upstream and method allowlists, bounded request bodies, timeouts, and a restrictive browser-security-header policy. API Gateway applies conservative throttling. Authenticated responses are dynamic and never enter shared caches.

Next.js must not:

- implement domain rules, application commands, persistence, job dispatch, or authoritative authorization;
- access PostgreSQL or Aurora;
- publish to SQS or invoke Batch;
- use S3 SDKs or AWS credentials;
- call LLM or embedding providers;
- expose Cognito tokens through the Auth.js client session;
- expose an unrestricted catch-all proxy to FastAPI.

Presigned S3 POST uploads and presigned downloads are the deliberate direct browser-to-AWS exception: FastAPI authorizes and creates the transfer through the BFF control plane, after which the browser transfers the binary directly with S3.

Place Vercel Functions close to the selected AWS API region. Vercel reaches FastAPI through public API Gateway and does not join the AWS VPC.

## Consequences

### Positive

- Authenticated request-time rendering and Server Components are available.
- Invite-only Cognito and managed MFA provide a useful baseline without custom account-management code.
- Cognito access and refresh tokens are not exposed to browser JavaScript.
- Same-origin BFF calls simplify browser authentication and centralize request hardening.
- FastAPI remains the single business contract and authorization boundary.
- Vercel Git integration provides Turborepo-aware previews and production deployments without another AWS runtime.

### Negative

- Vercel becomes a third-party hosting dependency.
- POLARIS operates a third runtime and adds a network hop between browser and FastAPI.
- Token renewal, concurrent refresh, revocation, and logout require a small amount of explicit handling.
- A concurrent refresh race can occasionally force the user to sign in again.
- Offline JWT validation cannot provide immediate invalidation of an already issued access token; the maximum exposure window is bounded by its 15-minute lifetime.
- Authorizer-context trust depends on IAM preventing direct API-function invocation by normal same-account principals.
- Cognito's fixed callback allowlist prevents arbitrary preview deployments from using production authentication.
- Deployment and observability are split across Vercel and AWS.
- User-specific data must be kept out of shared caches.
- Account provisioning and deprovisioning require a short maintainer runbook rather than a product administration UI.

## Rejected Alternatives

- **Static S3 and CloudFront Next.js export:** cannot provide the adopted server-side Auth.js session and BFF.
- **Vercel with browser-managed Cognito PKCE:** exposes token lifecycle management to browser JavaScript and bypasses the server-held session posture.
- **Expose Cognito access tokens through the Auth.js client session:** makes bearer tokens available to browser JavaScript.
- **Next.js as the business API:** creates a second application backend and authorization model.
- **Direct Vercel-to-Aurora access:** bypasses FastAPI, DDD, CQRS, workspace authorization, and VPC isolation.
- **Always-running AWS container for Next.js:** adds container, ingress, and idle-compute operations without a demonstrated requirement.
- **Auth.js database sessions or a distributed refresh lock:** add a datastore and operational dependency to avoid an occasional, recoverable reauthentication.
- **A prerelease Auth.js package for production:** makes a security-critical boundary depend on an unstable release contract without an MVP requirement.
- **Mandatory staging deployment:** duplicates cloud identity and data infrastructure before an external pilot or release process requires it.

## Review Triggers

Review this decision when:

- Vercel cost is materially higher than an equivalent supported deployment;
- data-residency rules cannot be met by the chosen Vercel region;
- measured BFF latency materially harms the user experience;
- web availability requirements diverge from Vercel's service characteristics;
- policy requires the web runtime to use private network connectivity to FastAPI;
- Auth.js and Cognito no longer interoperate safely for the required token lifecycle;
- the stable Auth.js line stops receiving security or selected-Next.js compatibility updates;
- invited-user or low-sensitivity-data assumptions no longer hold;
- an external pilot needs isolated authenticated acceptance testing;
- account volume or delegated administration makes the maintainer provisioning runbook impractical;
- POLARIS decides to self-host Next.js.
