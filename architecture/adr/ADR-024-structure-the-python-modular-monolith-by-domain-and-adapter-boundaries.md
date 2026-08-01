# ADR-024: Structure the Python Modular Monolith by Domain and Adapter Boundaries

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

ADR-001 establishes a modular monolith with explicit bounded contexts. The package root must therefore distinguish business capabilities from the technical code that starts and connects the application.

Placing bounded contexts beside `bootstrap`, `entrypoints`, and `infrastructure` mixes two classification schemes. Moving all non-domain code into `shared` would make the tree look tidier but would be misleading: runtime wiring is not a shared library, and a broad shared package tends to become a catch-all.

## Decision

Group bounded contexts under `contexts/` and the executable application shell under `runtime/`:

```text
polaris/
├── main.py
├── contexts/
│   ├── workspaces/
│   ├── policy_cases/
│   ├── knowledge/
│   ├── stakeholders/
│   ├── policy_documents/
│   ├── analysis/
│   └── evaluation/
└── runtime/
    ├── config.py
    ├── bootstrap/
    │   ├── api.py
    │   └── worker.py
    ├── entrypoints/
    │   ├── api/
    │   ├── worker/
    │   └── cli/
    └── infrastructure/
```

The responsibilities are:

- `contexts/` contains only bounded contexts and makes the business capabilities visible.
- `runtime/config.py` defines typed configuration without constructing services.
- `runtime/bootstrap/` is the composition root. It constructs dependencies, registers handlers, and assembles the API and worker runtimes.
- `runtime/entrypoints/` contains driving adapters for HTTP, worker messages, and operator commands.
- `runtime/infrastructure/` contains context-neutral technical foundations such as database session creation, cloud clients, and observability integration. It contains no business rules.
- `main.py` is a minimal import target for the selected process and contains no application wiring.

Do not create `shared/` initially. Add `shared/domain/` only when two or more bounded contexts genuinely require one domain concept with identical meaning and invariants. It is a deliberately governed shared kernel, not a home for utilities, transport models, configuration, or runtime infrastructure.

Each bounded context grows only the layers required by implemented behavior:

```text
contexts/policy_cases/
├── domain/
│   ├── policy_case.py
│   ├── events.py
│   ├── errors.py
│   └── repositories.py
├── application/
│   ├── commands/
│   ├── queries/
│   ├── dto.py
│   └── ports.py
└── adapters/
    ├── persistence/
    └── services/
```

Domain modules use cohesive domain names rather than generic files such as `aggregates.py` or `entities.py`. Context adapters implement context-owned ports. Transport schemas remain outside the contexts.

FastAPI concerns belong under `runtime/entrypoints/api/`, grouped by API area. This includes routers, authentication extraction, Pydantic request and response schemas, RFC 9457 Problem Details, and exception-to-HTTP mappings. Operational endpoints such as liveness belong under `runtime/entrypoints/api/system/`; they do not require artificial commands, queries, or domain models.

Dependencies follow these rules:

```text
runtime/bootstrap -> runtime/entrypoints, runtime/infrastructure, context adapters
runtime/entrypoints -> context application
context adapters -> context application and domain
context application -> context domain
context domain -> optional shared domain
```

- No context module imports `runtime`.
- `runtime/infrastructure` is context-neutral and does not import bounded contexts.
- Only bootstrap code selects and connects concrete adapters.
- Domain code imports only the standard library, its own context, and an explicitly approved shared-domain concept.
- One context does not import another context's aggregate or persistence adapter.
- Architecture tests enforce these boundaries.

Tests remain separate from source and are grouped by scope as they are introduced:

```text
tests/
├── unit/
├── contract/api/
├── integration/
├── end_to_end/
└── architecture/
```

Do not scaffold empty packages or placeholder layers.

## Consequences

### Positive

- The package root clearly separates business capabilities from runtime machinery.
- Framework, deployment, and transport concerns remain outside bounded contexts.
- A shared kernel cannot emerge accidentally as a utilities package.
- API and worker processes can share domain behavior without mixing their composition.

### Negative

- Import paths are slightly longer.
- `runtime/` requires discipline to remain an outer shell rather than an application-logic layer.
- Introducing a shared-domain concept requires an explicit architectural decision.

## Rejected Alternatives

- **Mix bounded contexts and technical packages at the root:** obscures which packages represent the domain.
- **Put bootstrap, entrypoints, and infrastructure under `shared/`:** labels application-specific runtime code as reusable shared code.
- **Create a shared kernel pre-emptively:** encourages speculative abstractions and hidden coupling.
- **Use global `domain/` and `application/` layers:** obscures bounded contexts and encourages cross-domain dependencies.
- **Place operational endpoints in a fake domain or `platform/presentation`:** gives transport concerns misleading domain ownership.

## Review Triggers

Review this decision if a bounded context is extracted into a separately deployed service, a second transport cannot use the existing runtime boundary cleanly, or architecture tests can no longer express the intended dependency direction.

## References

- [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
- [Architecture Patterns with Python: A Template Project Structure](https://www.cosmicpython.com/book/appendix_project_structure.html)
- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
