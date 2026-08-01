# ADR-022: Evolve and Recover Durable Data Without Destructive Releases

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Aurora PostgreSQL, S3 objects, audit records, and analysis provenance are authoritative POLARIS state. The application will evolve while Vercel and AWS deployments can temporarily run different compatible versions.

An in-place breaking migration can prevent rollback or make an active frontend incompatible with the API. Managed backups reduce risk but do not demonstrate that data and service can be restored within an acceptable period.

The portfolio deployment needs credible basic durability and recovery without multi-region infrastructure, continuous drills, or a staffed operations team.

## Decision

Use explicit, forward-oriented database migrations and expand-and-contract evolution:

- migrations never run during API, web, or worker startup;
- an approved deployment-only AWS Batch job applies migrations before code depends on the expanded schema;
- the migration job reuses the lightweight API image with a dedicated entry point and migration-only IAM and database role, runs inside the VPC, is submitted directly by CI, and is not reachable through product queues or Pipes;
- the first approved Terraform phase may register the migration job and compatible infrastructure expansion but does not advance active application digests; a successful migration gates the runtime-digest rollout;
- expansion changes remain compatible with the active and immediately preceding application versions;
- data backfills are restartable, observable, idempotent where practical, and bounded so they do not monopolize the database;
- code stops reading and writing obsolete structures before contraction removes them;
- destructive contraction occurs only after rollback no longer requires the old structure;
- deployment rollback normally restores compatible application code rather than executing destructive down-migrations;
- migration tests cover representative existing schemas and data, including partial backfill and retry behavior.

Preserve immutable source and versioned policy artifacts rather than updating them in place. Retention or authorized deletion is an explicit domain operation with an audit record.

For the portfolio deployment, use a single AWS region and target:

- a database recovery-point objective of no more than 15 minutes;
- a service recovery-time objective of no more than one business day;
- automated Aurora backups retained for at least 14 days;
- S3 versioning for source documents and important derived artifacts;
- expiration of noncurrent S3 versions for deleted content within 14 days;
- lifecycle rules based on artifact type, classification, and retention policy;
- versioned and locked Terraform state;
- documented recovery procedures with named prerequisites and validation steps.

These objectives do not promise recovery from permanent loss of the selected AWS region. A regional disaster is an explicit accepted risk for the MVP.

Complete one restoration rehearsal before storing non-demo user data and repeat it after a material change to storage, encryption, backup, or migration mechanisms. Verify application-level integrity, workspace isolation, artifact accessibility, audit records, and recovery-point timestamps rather than merely confirming that infrastructure exists.

Backup retention is not business-record retention. Content retention, audit retention, legal hold, workspace export, and deletion must be defined separately and applied consistently to PostgreSQL, S3, indexes, embeddings, and workflow checkpoints.

## Consequences

### Positive

- Schema changes remain compatible with staggered web, API, and worker deployments.
- The deployment pipeline can reach private Aurora without exposing the database or granting migration privileges to application runtimes.
- Rollback does not depend on unsafe reverse migrations.
- Restore capability is demonstrated before non-demo user data is accepted.
- Source and policy history remain recoverable and auditable.
- Recovery objectives are credible for a single-maintainer portfolio deployment without multi-region complexity.

### Negative

- Expand-and-contract can temporarily duplicate columns, tables, or write paths.
- Some changes require multiple releases.
- Backups, versions, and retained artifacts add storage cost.
- Restoration rehearsal and recovery documentation consume some engineering time.
- A regional disaster can exceed the stated objectives.
- Deletion must traverse multiple derived-data stores.

## Rejected Alternatives

- **Apply breaking migrations in place:** can make rollback and staggered deployment impossible.
- **Run migrations during application startup:** creates races, unpredictable cold starts, and excessive runtime privileges.
- **Require a down-migration for every change:** reverse data transformations can be unsafe or impossible.
- **Trust managed backups without restoration tests:** proves backup configuration, not recoverability.
- **Use event sourcing solely for recovery:** adds replay and evolution complexity without removing backup requirements.
- **Deploy multi-region active-active infrastructure for the MVP:** exceeds the availability requirement and one-maintainer operating capacity.

## Review Triggers

Review this decision when:

- a contractual recovery objective is stricter than the MVP targets;
- service availability commitments extend beyond a public portfolio deployment;
- regional continuity or data-sovereignty requirements arise;
- measured backup or restoration time approaches the recovery objective;
- data volume makes current backfill, versioning, or deletion strategies impractical;
- the deployment remains demonstration-only and no longer stores durable user data, in which case the recovery objectives may be reduced explicitly.
