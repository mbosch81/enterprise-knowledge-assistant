# Architecture and design decisions

## Request flow

```text
Question → authenticate the caller → search permitted documents
         → select evidence → return an answer with sources → record metrics
```

The HTTP API uses bearer-token authentication. The server maps the token to an authenticated identity and its tenant. A tenant is a separate document space, such as an organization or team. LangGraph runs the `knowledge_search` step, which calls the store with a tenant filter, checks the available evidence, and returns quotes or an abstention.

## Identity and access boundaries

FastAPI validates question length and rejects unknown request fields. Clients cannot supply their own tenant ID; token-to-tenant mappings are configured on the server.

This is a demonstration identity model. OpenID Connect (OIDC), roles, and document-level access control lists (ACLs) are not implemented. Each authenticated identity currently has access to all documents within its tenant.

## Retrieval and storage

`MemoryStore` supports fast offline tests. `PostgresStore` uses the same interface and parameterized SQL with pgvector cosine distance to rank vectors by similarity. The current vectors represent word overlap rather than semantic embeddings.

The database adapter performs an exact search over the permitted documents. Approximate search indexes such as HNSW, connection pooling, and asynchronous providers will be introduced only when measurements justify them. Database integration still requires a verified run.

The SQL adapter is intended for use behind the authenticated API. PostgreSQL row-level security (RLS) is not yet implemented as an additional database-enforced access boundary.

## Document processing and sources

Markdown text is split into chunks of up to 120 words, with a 20-word overlap between consecutive chunks. PDF extraction retains page references. Optical character recognition (OCR) and interpretation of table structure are not supported.

Chunk IDs are reproducible hashes. Re-ingesting an unchanged file does not create duplicates, but changed files currently require a fresh store to avoid retaining old chunks: previous versions are not automatically deleted.

Source references contain the original quote, filename, text position, and chunk ID. There is no endpoint for retrieving the original file and no immutable document archive.

## Bounded workflow and model use

LangGraph makes workflow state transitions explicit, although a simple function call would be sufficient for the initial baseline. A single read-only step and a recursion limit bound execution. Autonomous model planning, write actions, and approval state belong to later milestones.

The offline provider selects original sentences using word overlap. The optional Ollama provider selects from those candidate quotes using a local model. Returned quotes must exactly match the supplied evidence. This verifies their provenance, not their relevance or the completeness of the answer. Semantic retrieval remains a planned extension.

## Metrics and tracing

Structured logs record the request ID, latency, abstention decision, provider, reported model tokens, and model cost. Document content, questions, bearer tokens, and tenant names are excluded from these application metrics.

A zero model cost for offline or local inference means no per-call API fee; it does not include infrastructure, hardware, or electricity. External tracing is disabled by default. OpenTelemetry spans and further operational measurements are planned.

## Reference documentation

The following primary references were checked on October 14, 2026:

- [LangGraph StateGraph compilation](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
- [FastAPI security tools](https://fastapi.tiangolo.com/reference/security/)
- [pgvector documentation](https://github.com/pgvector/pgvector)

The resolved development dependencies are recorded in `requirements-snapshot.txt`. This is an environment snapshot, not a cross-platform lockfile. Container image and CI action digest pinning, along with automated dependency updates, remain open tasks.
