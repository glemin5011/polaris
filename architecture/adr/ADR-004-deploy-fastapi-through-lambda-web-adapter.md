# ADR-004: Deploy FastAPI through AWS Lambda Web Adapter

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

The synchronous API is expected to have low and irregular traffic. It must use the same FastAPI application locally and on AWS without embedding AWS Lambda concepts in domain or application code.

## Decision

Deploy the FastAPI ASGI application as a lightweight Lambda container behind API Gateway HTTP API using AWS Lambda Web Adapter.

Protect authenticated routes with API Gateway's JWT authorizer. API Gateway performs Cognito signature, issuer, expiry, app-client or audience, and route-scope validation before invoking Lambda. Lambda Web Adapter replaces any caller value and serializes the HTTP API v2 request context into `x-amzn-request-context`. A FastAPI adapter parses only the expected authorizer structure and fails closed when it is absent or malformed. FastAPI remains responsible for `token_use`, actor mapping, workspace membership, and domain authorization.

The Lambda resource policy grants `apigateway.amazonaws.com` invocation only from the configured API execution ARN. Normal human, application-runtime, CI, and deployment roles receive no direct `lambda:InvokeFunction` permission on the API function. This IAM restriction is part of the trust boundary because authorizer context is not independently cryptographic after it reaches Lambda; a same-account principal with direct invocation permission could forge an API Gateway-shaped event.

Pin the Lambda Web Adapter release in the API image. A deployed integration test must verify the expected authorizer-context shape and caller-header replacement before an adapter upgrade is accepted.

The API image includes synchronous application dependencies and excludes Docling, OCR, PyTorch, and heavyweight worker dependencies.

Run the same application locally with Uvicorn.

The authenticated Next.js BFF adopted by ADR-011 calls this API through public API Gateway. It does not replace FastAPI, run business use cases, or connect directly to the Lambda VPC.

## Consequences

### Positive

- No permanently running API tasks or load balancer.
- Local and deployed HTTP behavior share one ASGI application.
- FastAPI remains the OpenAPI source of truth.
- AWS integration stays in the runtime and infrastructure layers.

### Negative

- Cold starts remain possible.
- Lambda duration and concurrency limits apply.
- Database connections require bounded concurrency and conservative pooling.
- Long-running work must be delegated to background jobs.
- Adapter upgrades require verification of the request-context mapping used by authentication.
- Authorizer-context trust depends on preventing direct API-function invocation by normal same-account principals.

## Rejected Alternatives

- **Always-running Fargate API service:** higher idle cost and ingress overhead.
- **Lambda-specific handler implementation:** reduces local parity and leaks infrastructure into the application.
- **Next.js business API:** duplicates the backend and contract; the presentation-only BFF in ADR-011 is not a business API.

## Review Triggers

Review this decision when measured cold starts or database connection pressure violate the documented service objectives, Lambda limits block a required synchronous operation, a legitimate role requires direct API-function invocation, the adapter can no longer provide the verified authorizer-context mapping, or steady traffic makes an always-running service materially simpler or cheaper.
