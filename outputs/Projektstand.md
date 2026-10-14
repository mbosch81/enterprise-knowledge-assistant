# Enterprise Knowledge Assistant — project status

A personal learning project by Michael Bosch, exploring retrieval, evidence selection, bounded workflows, and evaluation.

## Observed results

- Initial automated tests: 8 passed. The guided VS Code run passed 8 tests in 0.33 seconds with Python 3.14.8; `pip check` reported no broken requirements.
- Offline evaluation: 5/5 synthetic cases passed. This small lexical baseline does not establish general model quality.
- One real local Ollama run with `qwen3:14b`: validated quote, 4.93 seconds, 332 reported model tokens. No cloud inference was used. See `ollama-live-result.json`; its private endpoint address has been redacted.
- The project owner built and started the API and PostgreSQL/pgvector through Docker Compose. PostgreSQL contained one `policies.md` chunk for tenant `demo`; the API returned the expected quoted answer. After a database restart, the chunk remained and the running API answered successfully.
- GitHub CI passed with Python 3.12. A subsequent run passed after updating actions and selecting Ubuntu 24.04.

These Docker and CI observations were reported by the project owner during the guided setup. They are distinct from automated database isolation tests, which remain outstanding.

## Next steps

Review the remaining project files, then improve Markdown handling through a focused test. Semantic embeddings, broader evaluation, PDF fixture tests, and automated PostgreSQL tenant-isolation tests remain open. This project does not claim production readiness or compliance certification.
