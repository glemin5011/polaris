# ADR-008: Store Source and Derived Documents in S3

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Policy source files and Docling artifacts can be large, immutable, and unsuitable for relational storage. The application still requires transactional metadata, searchable text, chunks, and citations.

## Decision

Store binary and large derived artifacts in S3 in AWS and behind a filesystem adapter locally.

Store in PostgreSQL:

- document metadata;
- versions and content hashes;
- processing state;
- structured sections;
- searchable chunks;
- embeddings;
- citations;
- object references.

Use short-lived S3 presigned POST policies and deterministic object keys. Each policy is scoped to one workspace, document, version, object key, allowed content type, and a `content-length-range` maximum. After upload, independently verify actual object size and metadata and compute or verify a SHA-256 hash before marking the version ready for processing.

New objects remain in a private pending-validation state and are not available for normal download or analysis until size, media type, file signature, hash, and processing-resource limits pass. Validated source downloads use an allowlisted response type and `Content-Disposition: attachment`; active browser-content formats are unsupported. The invited-user portfolio deployment does not require a malware-scanning service. Unsupported, encrypted, malformed, or unexpectedly expensive files fail closed.

## Consequences

### Positive

- Large files do not inflate PostgreSQL storage and backups.
- Direct browser uploads avoid routing file bodies through Lambda.
- Immutable artifacts support reproducibility and deduplication.
- Local development uses the same storage port without AWS.

### Negative

- Database and object-store consistency must be managed explicitly.
- Orphaned objects require cleanup.
- Access controls, object-state transitions, and presigned-upload constraints must be correct.
- Derived artifact formats require versioning.

## Rejected Alternatives

- **Store files in PostgreSQL:** increases database size, backup cost, and transfer overhead.
- **Expose S3 directly without an application abstraction:** couples domain workflows to AWS.

## Review Triggers

Review this decision when public or otherwise untrusted users may upload files, a supported format has a material parser vulnerability, storage cost exceeds its budget, or a customer requires malware scanning, object lock, legal hold, or customer-managed encryption keys.
