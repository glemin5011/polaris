# ADR-007: Use Aurora PostgreSQL and pgvector

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS needs transactional domain storage, read projections, full-text search, vector retrieval, background-job state, LangGraph checkpoints, and audit records. Operating separate databases for each concern would increase cost and consistency complexity.

## Decision

Use one Aurora PostgreSQL Serverless v2 cluster in AWS and PostgreSQL with pgvector locally.

Use separate schemas for bounded contexts and read models. Store:

- aggregate state;
- versioned metadata;
- full-text indexes;
- embeddings;
- read projections;
- background jobs and outbox records;
- LangGraph checkpoints;
- audit and evaluation data.

## Consequences

### Positive

- Relational, lexical, and vector queries share one transactional system.
- Local PostgreSQL closely matches production behavior.
- Metadata filtering and joins remain straightforward.
- Fewer managed services reduce operational overhead.

### Negative

- Aurora is the main fixed infrastructure cost.
- Vector and lexical workloads compete with transactional workloads.
- Large-scale retrieval may eventually require dedicated infrastructure.
- Supported PostgreSQL and pgvector versions must be pinned and tested.

## Rejected Alternatives

- **Dedicated vector database:** unnecessary service and consistency boundary.
- **OpenSearch at v0.1:** higher cost and operational scope.
- **Separate databases per bounded context:** distributed transactions without independent service ownership.
- **Aurora Data API as the primary repository interface:** weaker local parity with standard SQLAlchemy access.

## Review Triggers

Review this decision when connection pressure persists after bounded Lambda and worker concurrency, vector or lexical retrieval misses its measured latency objective, database cost exceeds the portfolio budget, or storage exceeds the practical scale of one Aurora cluster.
