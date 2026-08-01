# ADR-001: Use a Modular Monolith

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS is maintained by one developer, requires strict bounded contexts, and must run locally and on AWS with minimal operational overhead. Independent services would introduce network boundaries, distributed consistency, duplicated deployment concerns, and higher cost before they provide measurable value.

## Decision

Implement POLARIS as one Python modular monolith with:

- one repository;
- one domain and application codebase;
- one PostgreSQL cluster;
- explicit bounded-context packages;
- architecture tests that enforce module dependencies;
- separate API and worker runtime images built from the same codebase.

A bounded context may be extracted only when independent ownership, deployment, scaling, or availability requirements are demonstrated.

## Consequences

### Positive

- Local transactions remain available across application operations.
- Local development requires fewer processes and dependencies.
- Domain boundaries can be practised without distributed-system overhead.
- API and worker runtimes share types, rules, and release versions.

### Negative

- Module boundaries depend on code-level enforcement.
- Deployment changes affect the shared application release.
- Poor discipline could produce an unstructured monolith.

## Rejected Alternatives

- **Microservices:** unjustified operational and consistency overhead.
- **Unstructured monolith:** insufficient boundary enforcement and maintainability.

## Review Triggers

Review this decision when a bounded context needs independent ownership, deployment, availability, or scaling, or when a shared release repeatedly prevents safe delivery.
