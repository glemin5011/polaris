# ADR-015: Use Synchronous Projections by Default

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

CQRS read models must remain current enough for interactive policy editing. Making every projection asynchronous would introduce eventual consistency, relay dependencies, and additional failure handling.

## Decision

Update read projections in the same transaction as the command when the projection is small and deterministic.

Use asynchronous projection updates only when the source operation is already asynchronous or materially expensive, including:

- document processing;
- embedding generation;
- LLM analysis;
- evaluation runs.

## Consequences

### Positive

- Most user-facing reads are immediately consistent after commands.
- Projection failures roll back the command transaction.
- Local development and testing remain simple.
- No general-purpose projection worker is required.

### Negative

- Command transactions include projection work.
- Expensive projections must be identified and moved deliberately.
- Projection code must avoid cross-context aggregate loading.

## Rejected Alternatives

- **All projections asynchronous:** premature eventual consistency and operational overhead.
- **Query directly from aggregate tables for every screen:** couples UI queries to write models and aggregate structure.

## Review Triggers

Review this decision when measured projection work makes command latency unacceptable, a projection depends on an unavailable external system, or a rebuildable read model needs independent scaling.
