# ADR-005: Execute Background Work through AWS Batch on Fargate

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Docling, OCR, embedding generation, LangGraph workflows, consultation simulations, and evaluations may require more memory and execution time than synchronous API requests or Lambda workloads.

## Decision

Run heavyweight background jobs as AWS Batch jobs on Fargate.

Each task:

- receives a stable job identifier;
- loads job state from PostgreSQL;
- processes one job;
- writes results to PostgreSQL and S3;
- terminates after completion, failure, or a human-review checkpoint.

Use separate job definitions for document processing, analysis, and evaluation. They may share one compute environment.

Terraform sets an explicit maximum vCPU for the shared compute environment and bounded retry, timeout, CPU, and memory values for each job definition. The initial limits favor predictable portfolio-project cost over maximum throughput.

## Consequences

### Positive

- No idle worker fleet.
- Jobs receive explicit CPU and memory allocations.
- Heavy dependencies remain outside the API image.
- The same job runner can execute locally and in Batch.

### Negative

- Fargate startup latency applies to each job.
- Worker images are larger than the API image.
- At-least-once execution requires idempotent handlers.
- Very short jobs may be inefficient.

## Rejected Alternatives

- **Lambda workers:** unsuitable for heavyweight and variable-duration processing.
- **Always-running ECS workers:** unnecessary idle cost.
- **Kubernetes Jobs:** unjustified control-plane and operational overhead.

## Review Triggers

Review this decision when Batch startup time dominates measured job duration, a supported job cannot fit Fargate limits, sustained queue delay violates the job objective, or an always-running worker is demonstrably cheaper.
