# ADR-002: Apply Logical CQRS with One Database

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Commands and queries have different models and performance requirements. Separate services or databases would add distributed consistency, synchronization, and infrastructure costs that the initial workload does not require.

## Decision

Use logical CQRS inside the modular monolith:

- commands and queries use separate message types and handlers;
- command handlers load and modify aggregates through a unit of work;
- query handlers return purpose-built immutable DTOs;
- read models may use optimized SQL and cross-context projections;
- command and query data remain in one PostgreSQL cluster;
- CQRS terminology does not appear in public resource URLs.

## Consequences

### Positive

- Write-side invariants remain explicit.
- Query models can evolve independently from aggregates.
- Cross-context views do not require distributed joins or replication.
- Transactions remain local.

### Negative

- The codebase contains separate write and read models.
- Developers must prevent command handlers from returning page projections.
- Read-model synchronization rules must remain explicit.

## Rejected Alternatives

- **CRUD service layer:** mixes write invariants with UI-oriented reads.
- **Separate command and query databases:** premature replication and consistency overhead.
- **Separate command and query services:** unnecessary deployment boundary.

## Review Triggers

Review this decision when measured read or write load cannot be served by one PostgreSQL cluster, or when a context needs an independently owned consistency boundary.
