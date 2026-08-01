# ADR-013: Generate the TypeScript Client from OpenAPI

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

The Vercel Next.js server runtime and FastAPI backend require a stable, type-safe contract. Handwritten request clients duplicate schemas and permit silent drift.

## Decision

FastAPI generates the authoritative OpenAPI document.

Use `openapi-typescript` to generate path and schema types and `openapi-fetch` as the small typed runtime client. Pin both through the repository lockfile. Keep bearer-token attachment, the server-only API base URL, timeouts, correlation identifiers, and response handling in a thin application-owned client configuration rather than generated business logic.

The build pipeline must:

1. export `openapi.json` from FastAPI;
2. fail CI when the checked-in, versioned contract differs from that output;
3. lint the document and detect breaking changes;
4. generate the TypeScript schema types;
5. compile the `openapi-fetch` client configuration against those types;
6. compile the frontend against the typed client.

Every endpoint defines a stable `operation_id`, typed request and response models, documented errors, and authentication requirements. The generated OpenAPI document is not edited manually.

The generated client is used by the Vercel server runtime from React Server Components, explicit BFF Route Handlers, and thin Server Actions. Browser-interactive code calls the BFF rather than configuring the FastAPI base URL or Cognito bearer tokens.

The Vercel/Turborepo build generates the client from the checked-in versioned contract before building `apps/web`. Vercel and AWS have no implicit cross-platform deployment lock, so a frontend change that consumes a new API capability uses two delivery steps: deploy and smoke-test the backward-compatible API and versioned contract first, then merge or enable the frontend consumer. If both implementations coexist in one merge, the consumer remains disabled by a server-controlled feature flag until the API deployment succeeds. Breaking changes use expand-and-contract so active and immediately preceding web deployments remain operable.

## Consequences

### Positive

- Frontend types follow the deployed API contract.
- Breaking API changes become visible in CI.
- Request and response boilerplate is reduced.
- API documentation and client generation use one source.

### Negative

- Client generation becomes a required build step.
- Unstable operation IDs create unnecessary client changes.
- Generator upgrades may change generated types.
- Deployment ordering must preserve compatibility across independently deployed Vercel and AWS runtimes.
- A feature spanning both runtimes may require two merges or a temporary disabled feature flag.

## Rejected Alternatives

- **Handwritten fetch wrappers:** duplicate the contract and permit drift.
- **Manually maintained OpenAPI:** separates documentation from implementation.
- **Shared TypeScript/Python DTO package:** creates cross-language code-generation complexity without replacing OpenAPI.
- **Large generated SDK:** adds generated runtime code and upgrade churn when a typed native-fetch wrapper is sufficient.

## Review Triggers

Review this decision when the selected generator cannot represent a required OpenAPI feature, generated changes become unstable despite stable contracts, or another consumer requires a separately versioned SDK.
