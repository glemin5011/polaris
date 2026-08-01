# ADR-010: Use Local Adapters Instead of AWS Emulation

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

Local development must require no AWS account or cloud infrastructure. Emulating AWS services would add startup time, configuration, and behavior differences while still coupling development to AWS APIs.

## Decision

Define application ports and provide local adapters:

| Capability     | Local adapter                                                        | Deployed adapter                                      |
| -------------- | -------------------------------------------------------------------- | ----------------------------------------------------- |
| Blob storage   | Filesystem                                                           | S3                                                    |
| Job dispatch   | PostgreSQL queue                                                     | SQS                                                   |
| Job execution  | Local worker                                                         | AWS Batch                                             |
| Authentication | Development-only Auth.js identity provider and FastAPI auth adapter | Auth.js with Cognito                                  |
| Database       | PostgreSQL container                                                 | Aurora PostgreSQL                                     |
| Secrets        | Environment file                                                     | Vercel sensitive variables, Secrets Manager, or IAM  |
| LLM            | Ollama or provider API                                               | Bedrock or provider API                               |

Use Docker Compose only for PostgreSQL with pgvector and optional Ollama.

The local Auth.js provider issues a development identity that the FastAPI development-auth adapter can validate without Cognito or Vercel. Both sides require an explicit local-development mode and must fail closed when deployed. Development identity configuration is invalid in preview and production, and deployment checks must reject it.

## Consequences

### Positive

- Local startup remains fast and independent of AWS.
- Domain and application tests use stable ports.
- Cloud dependencies remain isolated in infrastructure adapters.
- Developers can work offline where model dependencies permit.

### Negative

- Local execution is not a byte-for-byte AWS simulation.
- Adapter contract tests are required.
- AWS-specific permissions and networking require deployed integration tests.

## Rejected Alternatives

- **LocalStack:** adds operational weight and incomplete service fidelity.
- **Mandatory sandbox AWS environment:** increases cost and slows development.
- **AWS SDK calls from application code:** prevents clean local substitution.
- **Using a production Cognito app client for local development:** makes local work depend on AWS and risks mixing development identity with deployed environments.

## Review Triggers

Review this decision when a production-only AWS integration cannot be represented by a deterministic local adapter and the resulting defect risk justifies a shared cloud integration environment.
