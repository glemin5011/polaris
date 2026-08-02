# ADR-017: Use a Transactional Outbox for Background Dispatch

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Commands that create background work must persist domain state and dispatch work reliably. Writing to PostgreSQL and SQS independently creates a dual-write failure window.

## Decision

Write the background job and outbox record in the same PostgreSQL transaction as the originating command.

After commit:

- attempt immediate publication to SQS;
- leave failed publications pending;
- use EventBridge Scheduler to invoke a dedicated relay entry point in the lightweight application image every five minutes;
- allow only one relay invocation at a time;
- claim a bounded batch with row locking that safely skips already claimed rows;
- retry transient failures with bounded backoff and mark repeatedly failing records for inspection;
- mark records published only after SQS accepts the message;
- monitor backlog age and retry count;
- retain published records for a short operational window before bounded cleanup.

Consumers remain idempotent because publication and delivery can both repeat.

## Consequences

### Positive

- Committed work cannot be lost because SQS publication failed.
- SQS outages do not roll back completed domain commands.
- Dispatch state is inspectable and recoverable.
- No distributed transaction is required.

### Negative

- Delivery is eventually consistent.
- Duplicate messages are possible.
- The relay and backlog require monitoring.
- Outbox retention and cleanup policies are required.
- Failed immediate publication may delay dispatch until the next five-minute relay run.

## Rejected Alternatives

- **Direct database-and-SQS dual write:** permits committed state without a job message.
- **Publish before database commit:** permits execution for rolled-back state.
- **Database polling as the production job queue:** unnecessary coupling when SQS and Batch are available.

## Review Triggers

Review this decision when outbox backlog age exceeds ten minutes under normal AWS availability, one bounded relay cannot keep up, relay polling becomes a material database cost, or another platform can preserve the database-to-message atomicity with less code.
