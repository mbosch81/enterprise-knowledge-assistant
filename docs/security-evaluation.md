# Security and evaluation

## Identity and tenant isolation

Tenant isolation is derived from server-side token configuration. Retrieval uses mandatory tenant filters. Clients cannot override the authenticated tenant through the request body. Tests cover these boundaries in the in-memory store and API; database isolation requires a separate integration test.

Configure tokens through local environment variables and never commit real credentials. The demonstration API binds to localhost. Production use would require TLS, secret management, OpenID Connect (OIDC), and rate limiting.

## Untrusted documents and prompt injection

Document content is untrusted input. The offline evidence-selection logic does not execute instructions found in text and has no write or network tools. A narrow pattern filter skips some obvious injection attempts. It is easy to bypass, may exclude legitimate text, and is not comprehensive prompt-injection protection.

The Ollama provider uses structured model output and accepts only exact quotes from the supplied evidence. This checks source provenance, not answer correctness or complete resistance to injection. Further work includes adversarial evaluation, separation of instructions from document data, and minimal tool permissions.

Authorized users can see document text in returned quotes. This is the intended data flow and must remain subject to access control.

## Evaluation and its limits

Retrieval is evaluated separately against expected sources. The offline answer check looks for expected substrings and evaluates whether the application correctly declines to answer when evidence is missing.

A passing case does not establish that an answer is complete or free of contradictions. The dataset is small and constructed from the demonstration documents, making the baseline results optimistic. Do not infer general model quality, robustness, or fairness from these results.

The error taxonomy includes:

- Missing relevant evidence during retrieval
- Irrelevant context
- Unsupported answers
- Incorrect source references
- Incorrect abstention decisions
- Cross-tenant data exposure
- Tool misuse

## Operational and regulatory context

Demonstrated technical measures include synthetic data, a server-side access boundary, reproducible tests, source references and reproducible chunk IDs, a bounded workflow, and metrics that exclude question and document content.

Open tasks include an independent audit, database row-level security (RLS), document access control lists (ACLs), retention and deletion, recovery testing, supplier risk assessment, operational procedures, and incident and change governance.

DORA and ISO 27001 provide possible context for exploring requirements in regulated environments. This project does not claim compliance or certification.
