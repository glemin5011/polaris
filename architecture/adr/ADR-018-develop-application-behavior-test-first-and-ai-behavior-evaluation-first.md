# ADR-018: Develop Application Behavior Test-First and AI Behavior Evaluation-First

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS contains deterministic application behavior and probabilistic AI behavior. Both require evidence before a change is considered complete, but they require different verification methods.

Tests written only after an implementation are biased toward the implementation that already exists. Exact-output tests for model responses are brittle and do not measure whether an analysis remains useful, grounded, safe, or affordable.

The project must remain maintainable by one developer. Its verification strategy therefore needs fast local feedback, a small number of high-value integration paths, and slower model evaluations outside the required pull-request path.

## Decision

Use strict red-green-refactor test-driven development for new deterministic behavior, bug fixes, behavior-changing refactors, and security controls:

1. describe one observable behavior;
2. write the smallest test that expresses it;
3. run the test and confirm that it fails for the expected reason;
4. write the minimum production code required to pass;
5. run the relevant test suite and confirm that it passes without warnings;
6. refactor only while the tests remain green.

A defect must first be reproduced by a failing regression test. Exploratory spikes are permitted only when their production implementation is discarded and rebuilt test-first.

Select the narrowest test boundary that proves the behavior:

- domain unit and property-based tests for invariants;
- application-handler tests for use-case behavior;
- PostgreSQL integration tests for repositories, transactions, projections, workspace scoping, constraints, and migrations;
- FastAPI and BFF contract tests for HTTP behavior;
- adapter contract tests for local and deployed infrastructure adapters;
- a small end-to-end suite for critical user journeys;
- architecture tests for dependency direction and runtime boundaries.

Tests should exercise real domain and application code. Use mocks only at genuine external boundaries where a real or deterministic fake implementation is impractical.

Use evaluation-driven development for prompts, retrieval, model selection, and other probabilistic behavior:

- version prompts, retrieval configurations, model identifiers, and evaluation datasets;
- use deterministic model doubles in the required pull-request pipeline;
- measure citation validity, evidence grounding, unsupported claims, observed-versus-inferred classification, stakeholder coverage, cost, and latency;
- compare proposed AI changes with an accepted baseline and block material regressions;
- run live-model evaluations separately with explicit credentials and controlled data;
- require human review before changing an accepted evaluation baseline.

Coverage is diagnostic rather than the definition of quality. Coverage must not materially decline, but the project does not require 100 percent line coverage. Apply mutation testing selectively to critical domain and authorization rules when it provides useful additional confidence.

Generated code is not tested internally. Its generation, compilation, compatibility, and use through application boundaries are tested. Declarative configuration may be exempt from test-first creation, but behavior that depends on it remains tested.

## Consequences

### Positive

- Tests demonstrate intended behavior rather than merely documenting an existing implementation.
- Defects receive permanent regression coverage.
- Test pressure encourages explicit ports and smaller use cases.
- Fast deterministic tests remain useful without model credentials.
- AI changes are evaluated against product qualities instead of exact wording.
- Refactoring remains safer for a single maintainer.

### Negative

- Initial implementation requires more discipline and test setup.
- Evaluation datasets and expected outcomes require maintenance.
- CI cannot prove that every developer observed the red phase.
- Model evaluations can vary and require carefully chosen thresholds.
- Some infrastructure behavior still requires deployed integration tests.

## Rejected Alternatives

- **Write tests after implementation:** loses the design and verification value of observing the expected failure first.
- **Use a coverage percentage as the primary quality gate:** rewards execution of lines rather than proof of behavior.
- **Test all behavior through the browser:** creates slow, fragile feedback and obscures failure causes.
- **Require live-model calls in every pull request:** makes normal CI slow, expensive, credential-dependent, and nondeterministic.
- **Use exact response snapshots for model output:** treats wording stability as product quality and produces brittle tests.
- **Apply mutation testing to the entire repository from v0.1:** adds disproportionate execution time and maintenance cost.

## Review Triggers

Review this decision when:

- required pull-request feedback regularly exceeds ten minutes;
- flaky tests materially reduce trust in the suite;
- AI evaluation results cannot support stable release decisions;
- the product adds model fine-tuning or automated high-impact actions;
- the team grows enough to require separate test ownership or release trains.
