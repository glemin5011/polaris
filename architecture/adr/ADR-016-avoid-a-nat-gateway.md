# ADR-016: Avoid a NAT Gateway

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

A NAT Gateway creates meaningful fixed cost for a low-traffic portfolio deployment. The API does not require outbound access to public LLM providers, while Batch workers do.

## Decision

Use:

- private subnets for Aurora;
- VPC-attached Lambda subnets for the API;
- public subnets with public IP assignment for ephemeral Fargate jobs;
- worker security groups with no inbound rules;
- an S3 gateway endpoint;
- an SQS interface endpoint;
- no NAT Gateway.

Workers use outbound internet access for external model providers and required public AWS endpoints. The API delegates all LLM operations to background jobs.

API Gateway's managed JWT authorizer retrieves and caches Cognito signing keys outside the Lambda VPC. FastAPI receives validated authorizer claims and therefore does not need public egress to retrieve Cognito JWKS. The API uses the S3 and SQS endpoints for its normal AWS data paths.

The Vercel web runtime adopted by ADR-011 reaches FastAPI through public API Gateway. It does not enter the VPC, so it does not require a NAT Gateway or change the private Aurora boundary.

## Consequences

### Positive

- Removes a significant fixed networking cost.
- Workers retain outbound access without exposing an inbound service.
- Database traffic remains private.
- API responsibilities remain lightweight.

### Negative

- Workers receive public network interfaces.
- Security-group and route-table configuration must be verified.
- Additional private AWS service access may require more VPC endpoints.
- A NAT Gateway may become necessary if future requirements prohibit public worker IPs.

## Rejected Alternatives

- **NAT Gateway from v0.1:** unjustified fixed cost.
- **Run external LLM calls from the API Lambda:** mixes long-running work with the synchronous path.
- **Private workers without NAT or endpoints:** cannot reach required external services.
- **FastAPI downloading Cognito JWKS through a NAT Gateway:** duplicates the managed API Gateway JWT authorizer and adds fixed networking cost.

## Review Triggers

Review this decision when the API requires a public outbound dependency that cannot move to a worker or use a VPC endpoint, policy prohibits public IPs on ephemeral workers, or the combined cost of required interface endpoints exceeds a NAT-based alternative.
