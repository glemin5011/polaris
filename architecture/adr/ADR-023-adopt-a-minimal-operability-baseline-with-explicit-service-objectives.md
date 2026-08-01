# ADR-023: Adopt a Minimal Operability Baseline with Explicit Service Objectives

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS spans a Vercel web and BFF runtime, a FastAPI Lambda runtime, an outbox relay, and Batch workers. A request or analysis can cross several of these runtimes before producing a result.

Structured logs and platform metrics without shared conventions or service objectives do not establish whether the system is healthy enough for a public portfolio deployment. Operating a self-managed observability platform would, however, add disproportionate work for one maintainer.

The project needs enough telemetry, limits, alarms, and recovery guidance to detect and diagnose material failures without promising continuous staffed support.

## Decision

Use OpenTelemetry concepts and stable semantic conventions for important request, job, metric, log, and resource names across TypeScript and Python. Use managed Vercel observability and Amazon CloudWatch. Do not require full distributed tracing or a self-managed OpenTelemetry collector for the portfolio deployment; correlation through structured logs is sufficient initially.

Propagate and record correlation and causation identifiers across:

- browser-visible error references;
- Vercel BFF requests;
- API Gateway and FastAPI;
- commands, queries, and database transactions;
- outbox records and SQS messages;
- Batch jobs and model invocations;
- audit records where correlation is useful.

Apply common resilience rules:

- every network operation has an explicit timeout;
- retries are limited to classified transient failures;
- backoff is bounded and includes jitter;
- unsafe operations are not retried unless an idempotency mechanism makes the retry safe;
- concurrency, job duration, document size, page count, model tokens, and model cost are bounded;
- dead-letter messages are inspectable and replayed only through an idempotent path;
- long-running jobs support defined timeout and cancellation behavior;
- degraded provider behavior produces a clear job or API state rather than an indefinitely running operation.

Telemetry is structured, bounded, and safe:

- use consistent runtime, service, operation, workspace, actor, job, analysis, model, and version fields;
- do not use high-cardinality or sensitive values as metric dimensions;
- do not record tokens, credentials, raw documents, prompts, retrieved evidence, or model responses by default;
- validate caller-supplied correlation identifiers before accepting them;
- distinguish operational telemetry from the domain audit trail.

Adopt initial internal service objectives for the portfolio deployment:

- at least 99.5 percent monthly success availability for authenticated control-plane requests, excluding announced maintenance and invalid client requests;
- p95 BFF-to-FastAPI duration below 1.5 seconds for ordinary operations that do not wait for background work or binary transfer;
- an alert for every dead-letter message and acknowledgement within one business day;
- no job may remain in `RUNNING` beyond its configured maximum duration without an alert and terminal recovery path;
- document-processing and consultation-run success and duration objectives are defined for published supported input envelopes before the public portfolio release;
- every analysis run has enforced token and cost budgets and observable actual consumption.

Measure control-plane success from eligible API Gateway and Vercel request outcomes, excluding authentication failures caused by invalid client input and announced maintenance. Measure BFF-to-FastAPI duration from Vercel server telemetry. These are engineering indicators rather than public commitments.

These objectives guide engineering and alerts; they are not contractual service-level agreements. The MVP does not promise continuous staffed support. Published service hours, maintenance expectations, and incident contact paths must reflect the actual support capacity.

Every production alert has the maintainer as owner, an actionable condition, and a short runbook. Maintain initial runbooks for:

- authentication or token-renewal failure;
- BFF or API outage;
- stuck, failed, or dead-lettered background work and provider degradation;
- database connection exhaustion or restoration;
- suspected cross-workspace disclosure or sensitive-data exposure.

## Consequences

### Positive

- Requests and jobs can be followed across both hosting platforms and all runtimes.
- Explicit objectives distinguish material reliability problems from incidental noise.
- Bounded time, concurrency, and model use protect reliability and cost.
- Managed telemetry avoids operating a separate monitoring platform.
- Runbooks reduce recovery time for a single maintainer.
- Sensitive application data remains out of telemetry by default.

### Negative

- Instrumentation must be maintained consistently in Python and TypeScript.
- Telemetry ingestion and retention incur cost.
- Service objectives require measurement and periodic calibration.
- Managed platforms may not provide a single cross-cloud trace view.
- One-maintainer support limits incident-response commitments.

## Rejected Alternatives

- **Use logs without shared context, metrics, or objectives:** makes multi-runtime diagnosis slow and health subjective.
- **Instrument every internal function:** creates noise, cost, and maintenance without proportional diagnostic value.
- **Operate Prometheus, Grafana, or an OpenTelemetry collector from v0.1:** adds infrastructure and on-call burden before managed backends prove insufficient.
- **Retry all external failures automatically:** can duplicate work, amplify incidents, and increase model cost.
- **Advertise a contractual SLA for the MVP:** is not credible without staffing, operational history, and customer requirements.
- **Create dashboards without associated decisions or alerts:** produces maintenance work rather than operational capability.

## Review Triggers

Review this decision when:

- a customer requires a contractual SLA or continuous support;
- incidents cannot be diagnosed using Vercel and CloudWatch;
- telemetry volume, cardinality, retention, or cost exceeds its budget;
- cross-cloud trace correlation is unreliable;
- multiple maintainers require formal on-call and incident-management processes;
- measured workload behavior requires different service objectives.
