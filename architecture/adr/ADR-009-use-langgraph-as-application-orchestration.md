# ADR-009: Use LangGraph as Application Orchestration

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Consultation analysis requires explicit multi-step workflows, checkpoints, bounded parallelism, and human review. The workflow engine must not replace the domain model or own business state.

## Decision

Use LangGraph as a worker-side orchestration adapter around application use cases. Domain and application packages do not import LangGraph types.

LangGraph nodes:

- call application ports and services through framework-neutral inputs and outputs;
- use identifiers and transient values as graph state;
- persist checkpoints in PostgreSQL;
- persist domain results through commands or application services;
- terminate at human-review interrupts and resume in a later worker job.

Graph state must not contain aggregates, ORM entities, database sessions, or credentials.

## Consequences

### Positive

- AI workflows are explicit, resumable, and testable.
- Human review does not require an active worker.
- Domain state remains independent of the orchestration framework.
- Nodes can use deterministic test doubles.

### Negative

- Workflow and domain state require explicit mapping.
- LangGraph upgrades may affect checkpoint compatibility.
- Developers must prevent framework concepts from leaking into bounded contexts.

## Rejected Alternatives

- **Step Functions for the same workflow:** duplicates LangGraph state and review semantics.
- **Unstructured autonomous agents:** weak reproducibility and evaluation.
- **Custom workflow engine:** unnecessary implementation burden.

## Review Triggers

Review this decision when checkpoint incompatibility prevents safe upgrades, workflow behavior cannot be tested without framework internals, or a managed workflow service would replace rather than duplicate LangGraph's responsibilities.
