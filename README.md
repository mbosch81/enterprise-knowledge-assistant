# Enterprise Knowledge Assistant – RAG & Agentic AI

A personal learning project by Michael Bosch, driven by curiosity about how AI applications work beyond a simple chat interface.

The goal is to explore document retrieval, evidence-based answers, bounded agent workflows, evaluation, and secure API design through hands-on development.

## Current status

The first working baseline reads synthetic documents, searches for relevant passages, and returns original quotes with source references. When it cannot find sufficient evidence, it declines to answer.

An initial local model run with Ollama has also been completed successfully. Retrieval currently relies on word overlap; semantic embeddings are the next development step.

This is an evolving learning project. PostgreSQL integration, broader evaluation, and production safeguards still require further implementation and verification. The existing implementation is an initial scaffold that will be reviewed and developed step by step.

### How the baseline works

1. **Ingestion:** read Markdown documents or PDFs containing extractable text.
2. **Chunking:** split text into reproducible, overlapping passages.
3. **Retrieval:** search for passages relevant to the question, restricted to the authenticated user's tenant.
4. **Evidence selection:** return matching original quotes and their source references.
5. **Abstention:** decline to answer when the available evidence is insufficient.

The offline baseline converts words into numerical vectors using a deterministic hash function. These are lexical vectors, not embeddings from a semantic model. Word overlap can miss paraphrases, and hash collisions can affect retrieval. The evidence check does not establish whether a passage fully answers the question.

FastAPI provides the HTTP API. A bounded LangGraph workflow performs one read-only knowledge search. It does not yet plan tasks autonomously. A PostgreSQL/pgvector adapter is implemented, but a database integration run remains outstanding.

## Local setup

Python 3.12 or newer is required. Development has been checked locally with Python 3.14; the Python 3.12 CI configuration has not yet been run on GitHub.

From the project directory:

```sh
python3 -m venv .venv
.venv/bin/pip install -e '.[test]'
export EKA_TOKENS='{"replace-with-a-random-local-secret":"demo"}'
.venv/bin/uvicorn eka.api:create_app --factory --host 127.0.0.1 --no-access-log
```

Use a randomly generated local secret instead of the example token. `EKA_TOKENS` maps bearer tokens to tenants on the server. Keep real credentials out of Git.

In a second terminal:

```sh
curl http://127.0.0.1:8000/ask \
  -H 'Authorization: Bearer replace-with-a-random-local-secret' \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many annual leave days?"}'
```

The expected answer contains **30 days**, a reference to `policies.md`, a chunk ID, and a text position. Asking `What is the CEO salary?` should produce an abstention.

Explore the API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Tests and evaluation

```sh
.venv/bin/pytest -q
.venv/bin/python -m eka.evaluate
```

The latest local run passed **8 tests** and **5 offline evaluation cases**. Tests cover API authentication, tenant isolation, reproducible ingestion, a narrow injection example, and validation of model-selected quotes.

The evaluation uses a small synthetic dataset. Passing it demonstrates baseline behavior, not general retrieval quality, model correctness, robustness, or fairness. CI runs without paid model calls.

## Local model with Ollama

Ollama must be reachable and have an installed text model. Set the endpoint and model for your environment before starting the API:

```sh
export EKA_PROVIDER=ollama
export OLLAMA_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=YOUR_INSTALLED_MODEL
export OLLAMA_TIMEOUT_SECONDS=90
```

Replace `YOUR_INSTALLED_MODEL` with an installed model name. The example URL assumes Ollama runs on the same machine. Environment variables must be exported explicitly for the host setup; the application does not automatically load `.env`.

The provider calls `/api/generate` with structured JSON output and a maximum of 256 output tokens. The configurable socket timeout defaults to 90 seconds; it is not a hard deadline for the whole request.

The model selects quotes from the existing lexical retrieval results. Returned quotes must exactly match the supplied evidence; invalid output produces HTTP 503. This verifies quote provenance, not whether the selected quote answers the question correctly. Documents remain untrusted input, and the current defenses do not provide comprehensive prompt-injection protection.

One real local run with `qwen3:14b` returned a validated quote in **4.93 seconds**, with **332 reported model tokens**. This demonstrates local LLM evidence selection, not a complete semantic RAG pipeline. Adding semantic embeddings through `/api/embed` is a planned next step.

Zero reported API cost for a local model excludes electricity and hardware costs. The local configuration uses a direct GPU endpoint. A separate shared endpoint in the development environment can fall back to a paid cloud API and is not the local-only default.

See the [Ollama API reference](https://github.com/ollama/ollama/blob/main/docs/api.md) and the environment-specific notes in [model-environment.md](docs/model-environment.md).

## PostgreSQL and pgvector

Docker is required for this setup. Configure a URL-safe random `POSTGRES_PASSWORD` and the `EKA_TOKENS` mapping, then run:

```sh
docker compose up --build
```

Compose reads local settings from `.env`; `.env.example` provides a starting point. Replace sample credentials before use. The API binds to localhost, and the database port is not published to the host.

The current table stores 256-dimensional lexical vectors. Setting `DATABASE_URL` activates the PostgreSQL adapter. A change to the embedding model or vector dimensions requires a migration strategy and re-ingestion.

The Compose setup has not yet been verified in an integration run. For Ollama in a container, configure an endpoint reachable from that container: `localhost` refers to the container itself.

## Documentation

The supporting documents are currently written in German. They are initial drafts and will be reviewed alongside the implementation.

- [Architecture and design decisions](docs/architecture.md)
- [Milestones and acceptance criteria](docs/milestones.md)
- [Security, evaluation, and operational boundaries](docs/security-evaluation.md)
- [Demo walkthrough](docs/demo.md)
- [Verification results](docs/verification.md)

## Data and license

The documents in `data/synthetic/` and the cases in `data/evaluation-v1.json` were created for this project. They describe fictional policies and contain no confidential company data.

Project code and synthetic data are available under the [MIT License](LICENSE). Any future third-party datasets will require documented sources and licenses.
