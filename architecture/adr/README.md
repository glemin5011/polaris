# POLARIS Architecture Decision Records

Architecture Decision Records document significant decisions that constrain the POLARIS architecture.

## Status Values

- **Proposed:** awaiting project acceptance.
- **Accepted:** active architectural constraint.
- **Deprecated:** retained for history but no longer recommended.
- **Superseded:** replaced by another ADR.
- **Rejected:** considered and not adopted.

## Index

| ADR | Decision | Status |
| --- | --- | --- |
| [ADR-001](ADR-001-use-a-modular-monolith.md) | Use a Modular Monolith | Accepted |
| [ADR-002](ADR-002-apply-logical-cqrs-with-one-database.md) | Apply Logical CQRS with One Database | Accepted |
| [ADR-003](ADR-003-do-not-use-event-sourcing.md) | Do Not Use Event Sourcing | Accepted |
| [ADR-004](ADR-004-deploy-fastapi-through-lambda-web-adapter.md) | Deploy FastAPI through AWS Lambda Web Adapter | Accepted |
| [ADR-005](ADR-005-execute-background-work-through-batch-on-fargate.md) | Execute Background Work through AWS Batch on Fargate | Accepted |
| [ADR-006](ADR-006-use-sqs-and-eventbridge-pipes-for-job-dispatch.md) | Use SQS and EventBridge Pipes for Job Dispatch | Accepted |
| [ADR-007](ADR-007-use-aurora-postgresql-and-pgvector.md) | Use Aurora PostgreSQL and pgvector | Accepted |
| [ADR-008](ADR-008-store-source-and-derived-documents-in-s3.md) | Store Source and Derived Documents in S3 | Accepted |
| [ADR-009](ADR-009-use-langgraph-as-application-orchestration.md) | Use LangGraph as Application Orchestration | Accepted |
| [ADR-010](ADR-010-use-local-adapters-instead-of-emulation.md) | Use Local Adapters Instead of AWS Emulation | Accepted |
| [ADR-011](ADR-011-deploy-nextjs-on-vercel-as-an-authenticated-bff.md) | Deploy Next.js on Vercel as an Authenticated BFF | Accepted |
| [ADR-012](ADR-012-keep-business-apis-out-of-nextjs.md) | Keep Business APIs out of Next.js | Accepted |
| [ADR-013](ADR-013-generate-the-typescript-client-from-openapi.md) | Generate the TypeScript Client from OpenAPI | Accepted |
| [ADR-014](ADR-014-use-python-3.13-with-strict-static-typing.md) | Use Python 3.13 with Strict Static Typing | Accepted |
| [ADR-015](ADR-015-use-synchronous-projections-by-default.md) | Use Synchronous Projections by Default | Accepted |
| [ADR-016](ADR-016-avoid-a-nat-gateway.md) | Avoid a NAT Gateway | Accepted |
| [ADR-017](ADR-017-use-a-transactional-outbox-for-background-dispatch.md) | Use a Transactional Outbox for Background Dispatch | Accepted |
| [ADR-018](ADR-018-develop-application-behavior-test-first-and-ai-behavior-evaluation-first.md) | Develop Application Behavior Test-First and AI Behavior Evaluation-First | Accepted |
| [ADR-019](ADR-019-build-an-accessible-and-international-ready-web-interface.md) | Build an Accessible and International-Ready Web Interface | Accepted |
| [ADR-020](ADR-020-enforce-secure-development-and-database-backed-workspace-isolation.md) | Enforce Secure Development and Database-Backed Workspace Isolation | Accepted |
| [ADR-021](ADR-021-govern-sensitive-data-and-preserve-ai-analysis-provenance.md) | Govern Sensitive Data and Preserve AI Analysis Provenance | Accepted |
| [ADR-022](ADR-022-evolve-and-recover-durable-data-without-destructive-releases.md) | Evolve and Recover Durable Data Without Destructive Releases | Accepted |
| [ADR-023](ADR-023-adopt-a-minimal-operability-baseline-with-explicit-service-objectives.md) | Adopt a Minimal Operability Baseline with Explicit Service Objectives | Accepted |

## Process

1. Copy `ADR-TEMPLATE.md`.
2. Allocate the next sequential number.
3. Record one significant decision.
4. Describe concrete consequences and rejected alternatives.
5. Update this index.
6. Do not rewrite accepted ADR history. Supersede it with a new ADR.
