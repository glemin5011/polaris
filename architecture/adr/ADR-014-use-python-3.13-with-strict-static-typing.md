# ADR-014: Use Python 3.13 with Strict Static Typing

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS is a learning and portfolio project focused on advanced Python design, explicit contracts, and maintainability. Dynamic or weakly typed boundaries would undermine those goals.

## Decision

Use Python 3.13 with:

- `uv` for dependency and environment management;
- Ruff for linting and formatting;
- Pyright in strict mode;
- typed SQLAlchemy 2 and Pydantic 2 APIs;
- `Protocol` for ports;
- immutable command and query DTOs;
- no untyped public functions;
- no unexplained `Any`;
- property-based tests for domain invariants;
- architecture tests for module boundaries.

Pin the Python minor version across local development, containers, and CI.

## Consequences

### Positive

- Application contracts are checked before runtime.
- Refactoring across bounded contexts is safer.
- Infrastructure dependencies remain explicit.
- The codebase demonstrates modern Python practices.

### Negative

- Some third-party libraries require stubs or typed adapters.
- Strict typing adds implementation effort.
- Runtime upgrades require dependency validation.

## Rejected Alternatives

- **Untyped or partially typed Python:** inconsistent with project goals.
- **Immediately adopting the newest unsupported Python minor:** unnecessary dependency risk.
- **Pydantic models as domain entities:** couples the domain to serialization and validation frameworks.

## Review Triggers

Review this decision when Python 3.13 leaves upstream security support, a required dependency cannot support it, or the chosen type checker prevents adoption of a necessary library without a safe typed boundary.
