# Prioritized development milestones

These milestones guide a personal learning project. They describe measurable goals rather than claims of production readiness. The initial implementation is a scaffold to review and develop step by step.

## M1 — End-to-end offline baseline

The baseline is implemented and has passed local tests; see [verification results](verification.md).

Acceptance criteria:

- Ingestion produces reproducible chunks.
- An authenticated HTTP question returns an answer with source references.
- Missing evidence leads to abstention: the application declines to answer.
- CI tests require no paid model calls.
- Local setup and the demo are reproducible from documented instructions.

A guided Docker run confirmed startup, a quoted API answer, and persistence and API access after a database restart. Persistence after an API restart and automated tenant-isolation checks against the actual database remain outstanding.

## M2 — Semantic RAG demo (next priority)

A first local Ollama inference run is documented. Semantic embeddings and a complete semantic RAG evaluation remain outstanding.

Acceptance criteria:

- Define interfaces for embeddings and model responses, with timeouts, token limits, and provider-appropriate usage accounting.
- Use the selected local Ollama environment. A cloud provider requires an explicit decision about data transfer and budget; never put API keys in chat or Git.
- Record at least one real end-to-end run using semantic retrieval and a model.
- Add a test PDF and at least 30 versioned evaluation cases covering answerable and unanswerable questions, paraphrases, conflicting evidence, and evidence spanning multiple pages.
- Measure retrieval separately from answer quality. Initial targets on this dataset: recall@3 of at least 0.90, valid source references of at least 0.95, and correct abstention decisions of at least 0.90.
- Record model, prompt, and dataset versions alongside results, latency, and costs.

Recall@3 measures whether relevant evidence appears among the first three retrieved results. Valid references establish source provenance; they do not by themselves establish answer correctness. Define the scoring rules before evaluating. Results on this limited dataset are not a general quality guarantee.

## M3 — Security boundaries

Acceptance criteria:

- Introduce verified identities through OpenID Connect (OIDC), document-level access control lists (ACLs), and PostgreSQL row-level security (RLS) as an additional boundary.
- Automate cross-tenant tests against a real database.
- Evaluate at least ten adversarial documents and ten adversarial questions.
- Test that logs do not expose document content or secrets.
- Enforce upload-size and PDF-page limits when an upload endpoint is introduced.
- Document remaining attack scenarios and a deletion and re-ingestion strategy.

Prompt-injection tests demonstrate observed behavior, not complete protection.

## M4 — Bounded agent and verifiable approvals

Acceptance criteria:

- Provide at least two distinct, useful read tools: knowledge search and document metadata lookup.
- Limit execution to at most three model/tool steps, with timeouts and an explicit list of permitted tools.
- Add an optional write tool only when approval is persistent, tied to the authenticated identity, valid for the exact proposed arguments, and usable once.
- Test replayed approvals, modified arguments, and attempts by another identity to use an approval.

Until those approval requirements are met, the workflow remains read-only.

## M5 — Operations and reproducible demo

Acceptance criteria:

- Add local OpenTelemetry traces without prompt or document content. Enable external Langfuse tracing only through deliberate configuration.
- Measure median (p50) and p95 latency under a defined workload.
- Test provider failures and timeouts. For any paid provider, enforce a budget before and during evaluation runs.
- Explore fairness using paired questions with the same underlying meaning but different names, pronouns, or languages. Compare answerability, sources, and error rates; document the limits of this operational definition.
- Add a database integration job to CI and document a five-minute demo. The container build has passed a manual local check; automated build verification remains planned.

The five baseline policy questions do not establish demographic fairness. Local inference has no per-call API fee, but hardware and electricity still have costs.

## Implementation order

First establish semantic retrieval, a real end-to-end model run, and database integration evidence. Then expand access controls, agent capabilities, and operational measurements.

DORA and ISO 27001 may provide useful context when exploring requirements for regulated environments. This project does not assess legal applicability or claim compliance or certification.
