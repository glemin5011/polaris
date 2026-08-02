# ADR-006: Use SQS and EventBridge Pipes for Job Dispatch

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

The API must enqueue background work reliably without running a permanent queue consumer or implementing infrastructure glue that AWS already provides.

## Decision

Use:

- SQS as the durable production job queue;
- separate queues for document processing, analysis, and evaluation;
- EventBridge Pipes to map SQS messages to AWS Batch `SubmitJob`;
- a Pipe source batch size of one so each queue message creates one Batch job;
- dead-letter queues for exhausted deliveries;
- messages containing identifiers and metadata only.

All consumers assume at-least-once delivery.

Submit one Batch job per SQS message. Terraform sets bounded Pipe concurrency, queue visibility timeouts longer than the supported job-submission attempt, a finite retry policy, and a dead-letter queue with an alarm. Batch maximum vCPU provides the final cost and concurrency bound.

## Consequences

### Positive

- Durable buffering separates API traffic from worker capacity.
- EventBridge Pipes removes a custom queue-consumer Lambda.
- Queue depth provides backpressure and operational visibility.
- Workload categories can scale independently.

### Negative

- Duplicate delivery is possible.
- Pipe and Batch failures require monitoring.
- Message contracts must remain backward compatible.
- Ordering is not guaranteed unless explicitly configured.

## Rejected Alternatives

- **Direct API-to-Batch calls:** couples request handling to compute submission and weakens retry guarantees.
- **Custom SQS consumer Lambda:** additional code and failure modes.
- **Kafka:** excessive operational scope.
- **Step Functions:** duplicates workflow concerns owned by LangGraph.

## Review Triggers

Review this decision when measured queue delay or throughput exceeds the Batch submission path, ordering becomes a business requirement, or Pipe failures are harder to operate than a small purpose-built consumer.
