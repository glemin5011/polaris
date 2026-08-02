# ADR-020: Enforce Secure Development and Database-Backed Workspace Isolation

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS stores workspace data in one PostgreSQL database. The portfolio deployment is limited to the public, synthetic, and ordinary low-sensitivity content defined by ADR-021. FastAPI is the authoritative business-authorization boundary, but an omitted workspace predicate could still expose or modify another workspace's data.

Workspace isolation affects identifiers, keys, repositories, transactions, background jobs, audit records, storage paths, tests, and database roles. Retrofitting these controls after data exists would be expensive and risky.

The project needs a practical secure-development baseline that one maintainer can operate without establishing a compliance program or reproducing enterprise defense in depth.

## Decision

Use NIST Secure Software Development Framework 1.1 as an organizing reference and OWASP Application Security Verification Standard 5.0.0 as a risk checklist. Apply requirements that protect the documented deployment and record important exclusions; do not claim ASVS Level 2 compliance or certification.

Maintain a short security checklist for authentication, authorization, uploads, secrets, dependencies, logging, backups, and deployment. It may live with the architecture or release checklist and does not require a governance platform.

Require a focused threat model when a feature introduces or materially changes:

- an authentication, session, or authorization path;
- a trust boundary or privileged operation;
- an external provider or webhook;
- a supported upload or document format;
- processing of a new data classification;
- an operation that can affect another system or workspace.

Enforce workspace ownership through a small set of consistent controls:

- every workspace-owned row has a non-null `workspace_id`;
- tenant-scoped uniqueness constraints include `workspace_id` where the value is not globally unique;
- foreign keys between workspace-owned records include workspace scope where practical, preventing cross-workspace relationships;
- application ports and repository methods require workspace context explicitly;
- FastAPI resolves membership and authorizes every business operation;
- jobs, outbox records, checkpoints, projections, audit events, and blob references retain workspace scope;
- every protected operation has a negative cross-workspace test;
- the API and worker use runtime database roles without schema-changing privileges;
- migrations use a separate role and never run from application startup;
- raw SQL that accesses workspace-owned data requires an explicit workspace predicate and integration coverage.

PostgreSQL row-level security is not part of this deployment. Mandatory repository scoping, tenant-aware constraints, narrow database roles, FastAPI authorization, and negative integration tests provide proportionate protection for an invited-user POC and avoid transaction-context and migration complexity.

Apply the following inexpensive deployment controls:

- private Aurora subnets, encrypted private S3 buckets, TLS, and least-privilege IAM;
- invite-only Cognito accounts and required MFA as defined by ADR-011;
- Auth.js CSRF protection for authentication routes, application CSRF tokens and origin validation for state-changing BFF Route Handlers, Next.js same-origin enforcement and entry-point authentication for Server Actions, secure cookies, a restrictive Content Security Policy, and standard browser security headers;
- bounded request bodies, API Gateway throttling, and explicit timeouts;
- secret scanning, dependency vulnerability checks, and container-image scanning in CI or managed platform services;
- no secrets, authorization tokens, raw documents, prompts, or retrieved evidence in normal logs.

The initial role model remains deliberately small. Enterprise attribute-based access control, policy engines, separate customer databases, and customer-managed keys are not part of the MVP.

## Consequences

### Positive

- Workspace isolation is enforced at the API, application, repository, schema-constraint, and test layers.
- Tenant-aware keys prevent invalid cross-workspace relationships.
- The baseline addresses common high-impact risks without requiring certification bureaucracy.
- Separate migration and runtime roles limit application privileges.

### Negative

- Application code must apply workspace scope consistently.
- Composite constraints can make schemas and joins more verbose.
- The security checklist and focused threat models require modest maintenance.
- A missing predicate remains possible despite structural APIs and tests.

## Rejected Alternatives

- **Adopt PostgreSQL row-level security immediately:** adds transaction context, policy, role, migration, connection-reuse, and test complexity that is disproportionate for the restricted invited-user POC.
- **Rely on ad hoc query filters:** makes workspace scope optional and too easy to omit; repositories and ports instead require it structurally.
- **A separate database or schema per workspace:** creates disproportionate migration, pooling, backup, and operational cost for the MVP.
- **Adopt enterprise ABAC or an external policy engine immediately:** adds policy infrastructure before the product has a corresponding authorization model.
- **Depend on the Next.js BFF for authoritative authorization:** the BFF is a presentation boundary and cannot protect direct API calls.
- **Claim framework compliance:** formal assurance requires evidence and independent verification beyond a portfolio deployment.

## Review Triggers

Review this decision when:

- an external organization relies on POLARIS as a real multi-tenant service;
- application content becomes legally privileged, high impact, or subject to sector-specific or heightened privacy requirements;
- a cross-workspace defect or near miss reveals that structural scoping is insufficient;
- customers require database, account, or encryption-key isolation;
- the authorization model grows beyond a small, understandable role set;
- a formal security assessment or certification introduces additional controls.
