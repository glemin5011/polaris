# ADR-012: Keep Business APIs out of Next.js

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS uses FastAPI to practise Python DDD, CQRS, LangGraph integration, and typed OpenAPI contracts. Implementing business endpoints in Next.js would create two backend stacks and ambiguous ownership.

## Decision

FastAPI is the only business application API.

ADR-011 adopts Next.js as an authenticated presentation BFF. Next.js may:

- manage Auth.js login, callback, logout, session cookies, and Cognito token renewal;
- attach the server-held Cognito access token to allowlisted FastAPI requests;
- perform request-time rendering and presentation-specific aggregation;
- expose explicit presentation-facing Route Handlers and thin Server Actions;
- use the generated OpenAPI client to call FastAPI.

Next.js must not:

- access PostgreSQL;
- publish to SQS;
- invoke Batch;
- use S3 SDKs or AWS credentials;
- call LLM providers for application use cases;
- implement domain commands, business rules, persistence, or authoritative authorization;
- expose Cognito access or refresh tokens to browser JavaScript;
- expose an unrestricted generic proxy to FastAPI.

All authenticated control-plane browser requests pass through the adopted BFF. Presigned binary transfers are the only normal direct browser-to-AWS exception and must first be authorized by FastAPI.

## Consequences

### Positive

- One domain boundary and authorization model.
- One authoritative API contract.
- No duplicated DTOs, validation, or persistence logic.
- Backend development remains concentrated in Python.

### Negative

- BFF requests add a network hop before reaching FastAPI.
- Presentation adapters require discipline to remain thin.
- Presentation aggregation may still require dedicated FastAPI queries when it encodes reusable business meaning.

## Rejected Alternatives

- **Next.js Route Handlers as the primary API:** duplicates business logic and contracts.
- **Direct database access from Next.js:** bypasses the domain and command model.
- **Unrestricted reverse proxy:** weakens route, size, header, and audit controls.

## Review Triggers

Review this decision when a presentation-specific capability cannot be expressed through the FastAPI contract without harming that contract, and only after documenting why it is not a domain or application use case.
