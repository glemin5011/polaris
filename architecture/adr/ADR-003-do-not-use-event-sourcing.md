# ADR-003: Do Not Use Event Sourcing

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS requires versioned policy artifacts, reproducible analysis runs, audit records, and reliable asynchronous dispatch. It does not require reconstruction of all aggregate state from an event stream.

## Decision

Persist current aggregate state using conventional relational tables.

Use:

- immutable domain events for in-process reactions;
- a transactional outbox for external dispatch;
- explicit document and profile versions;
- append-only audit records for user and policy actions.

Do not use event streams as the primary persistence model.

## Consequences

### Positive

- Persistence and migrations remain conventional.
- Queries and debugging use current relational state.
- Auditability is implemented only where required.
- Aggregate loading does not require event replay.

### Negative

- Historical state must be preserved through explicit version tables.
- Domain events cannot recreate every prior aggregate state.
- Temporal queries require purpose-built history models.

## Rejected Alternatives

- **Event sourcing:** adds replay, event-versioning, projection recovery, and migration complexity without a current requirement.

## Review Triggers

Review this decision only when rebuilding aggregate state from a complete event history becomes a demonstrated product requirement that explicit versions and audit records cannot satisfy.
