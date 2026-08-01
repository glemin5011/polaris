# ADR-021: Govern Sensitive Data and Preserve AI Analysis Provenance

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS is a portfolio POC that demonstrates policy-document analysis. Application content is limited to public, synthetic, and ordinary low-sensitivity internal material. Personal data is limited to the minimum invited-account identity required for access and public professional information used as evidence. It is not designed to carry classified, legally privileged, credential-bearing, special-category, non-public personal, or high-impact sensitive content. Selected permitted content may be retrieved and sent to approved model providers for embeddings or generation.

Authentication, workspace isolation, and encryption do not decide which information may leave the system, which provider may process it, how long it may be retained, or whether an analysis can later be reconstructed. Uploaded documents and retrieved text can also contain malicious or irrelevant instructions intended to manipulate model behavior.

The MVP needs enforceable controls without building a general data-loss-prevention or model-governance platform.

## Decision

Use a small fail-closed information-classification model:

- `PUBLIC`: approved for public disclosure;
- `INTERNAL`: ordinary low-sensitivity material limited to authorized workspace members and approved service providers; it excludes private correspondence and non-public personal datasets;
- `RESTRICTED`: unsupported by the portfolio deployment and rejected before storage or processing when identified.

Each workspace defaults to `INTERNAL`. Documents have an explicit classification, and derived artifacts inherit the source classification. Classification changes are authorized and audited operations. Product copy clearly states the unsupported-data boundary before upload.

Publish a short privacy notice before inviting non-maintainer users. It identifies the minimal account data collected, its purpose, the Vercel, AWS Cognito, and approved model-provider processing paths, the retention boundary, and the contact for access or deletion requests.

Keep model-provider policy in server configuration. An approved entry defines:

- permitted data classifications;
- permitted processing regions;
- approved model identifiers and capabilities;
- retention, training, and data-use requirements;
- whether embeddings, reranking, generation, or another operation is allowed;
- request, token, timeout, and cost limits.

Reject a model invocation when no approved provider satisfies the effective classification and operation. Provider configuration is not a browser concern and cannot be overridden by user-supplied request data.

Place newly uploaded documents in a pending-validation state. Before conversion, indexing, retrieval, or model processing, validate:

- declared size and actual size;
- supported media type and file signature;
- decompression, page, image, and processing-resource limits;
- content hash and workspace ownership.

The POC does not run a malware-scanning service. Uploads are restricted to invited users and a small supported-format list. Objects remain private, source downloads use an allowlisted response type and forced attachment disposition, and active browser-content formats are unsupported. Encrypted, malformed, oversized, unsupported, or out-of-budget files fail closed. Public or untrusted uploads require a new threat model and managed malware-scanning decision.

Treat user input, documents, retrieved passages, model responses, and provider metadata as untrusted data:

- retrieved content cannot modify system instructions or grant authority;
- model output cannot invoke a privileged operation directly;
- external references and model-suggested URLs are not fetched without an explicit safe adapter and policy;
- model output crosses application boundaries through typed, validated structures;
- citations must resolve to authorized, versioned evidence;
- consequential state changes use normal authenticated commands and require human approval where the workflow defines it.

Persist sufficient provenance for every material analysis result:

- model provider and model identifier;
- prompt and workflow versions;
- retrieval, embedding, chunking, and reranking profiles;
- source document, stakeholder-profile, and evidence versions;
- material generation parameters;
- citations and citation-validation outcome;
- observed-versus-inferred classification and confidence;
- human review, correction, and approval;
- execution time, token use, estimated cost, and relevant correlation identifiers.

Provide an owner-authorized workspace deletion operation before storing non-demo data. It removes active access to source and derived artifacts, indexes, embeddings, and checkpoints; provider-side deletion is requested where supported. Noncurrent S3 versions and encrypted database backups expire within 14 days. The POC does not promise legal hold, records-management compliance, or a formal portability export.

Operational telemetry must not become a secondary document or prompt store. Raw documents, retrieved passages, prompts, model responses, personal data, credentials, and authorization tokens are excluded from logs and traces by default.

## Consequences

### Positive

- Sensitive-data egress is controlled by an explicit server-side policy.
- Restricted information fails closed instead of silently reaching an external model.
- Analysis results can be traced to their evidence, configuration, model, and human review.
- Pending validation and resource limits reduce file-processing risk.
- Typed model boundaries constrain prompt injection and unsafe output handling.
- Retention and deletion become product behavior rather than manual storage cleanup.

### Negative

- Some documents cannot use every model or may not be processable in the MVP.
- Provider onboarding requires security and data-use review.
- The limited data classification prevents some otherwise plausible demonstrations.
- Provenance consumes storage and must evolve compatibly.
- Derived-artifact deletion is more complex than deleting a single document row.
- Human review limits full automation.

## Rejected Alternatives

- **Send all data to the configured model provider:** ignores confidentiality, regional, retention, and contractual differences.
- **Use free-form classification labels:** prevents consistent enforcement and testing.
- **Rely on prompts to prevent prompt injection:** instructions cannot turn untrusted content into trusted control data.
- **Allow model output to perform business actions:** grants probabilistic output excessive authority.
- **Log complete prompts and retrieved evidence for debugging:** creates an uncontrolled secondary store of sensitive information.
- **Retain every source and derived artifact indefinitely:** conflicts with minimization, customer deletion, and storage governance.
- **Build a general DLP platform for the MVP:** exceeds the needs and operating capacity of one maintainer.
- **Require malware scanning for invited POC uploads:** adds infrastructure without a public or untrusted upload path; the decision must be revisited before that assumption changes.

## Review Triggers

Review this decision when:

- anyone proposes classified, privileged, non-public personal, sector-regulated, or otherwise high-impact sensitive application content;
- uploads become public or are accepted from untrusted users;
- a new model provider, processing region, or provider capability is introduced;
- POLARIS gains tools capable of external side effects;
- legal, contractual, or records-management requirements change;
- the three-level classification model cannot express required policy.
