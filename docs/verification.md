# Verification record — October 14, 2026

This record distinguishes executed checks from prepared configurations. Results describe specific runs, not production readiness.

## Initial development checks

- Environment: Python 3.14 in a fresh virtual environment.
- Automated tests: **8 passed in 0.19 seconds** after configuration changes.
- Offline evaluation: **5/5 cases passed**. Expected sources were retrieved for 3/3 answerable cases; 2/2 unanswerable cases produced abstention. This small synthetic baseline does not establish general quality.
- FastAPI was exercised through an ASGI test client: a grounded answer, missing and invalid tokens, an attempted client-side tenant override, and a cross-tenant question.
- Reproducible ingestion and a narrow, obvious prompt-injection example were tested.
- Simulated Ollama responses tested exact-quote selection, token accounting, and rejection of invented evidence. These protocol tests do not call a real model.

## Real local model run

The remote RTX 4090 endpoint returned `qwen3:14b` through `/api/tags`.

A real Ollama provider run using a synthetic annual-leave policy returned **30 days** with an exactly validated original quote. The run took **4.93 seconds** and reported **332 model tokens**. The result is recorded in `outputs/ollama-live-result.json`.

This single run demonstrates local inference and quote validation. It does not establish general model quality or semantic retrieval. No cloud inference request was made.

During the initial environment check, no Ollama command or service was found on localhost. The subsequent successful run used a remote LAN endpoint; local installation was not required.

## Guided development environment setup

The project owner completed the setup in VS Code using a project-local `.venv` with **Python 3.14.8** and reported:

- `python -m pip check`: **No broken requirements found.**
- `python -m pytest -q`: **8 passed in 0.33 seconds**.

The repository was initialized on `main`. The initial commit, README, project configuration, environment template, demo walkthrough, milestones, and architecture document were committed and pushed to GitHub during the guided setup. These uploads do not establish that GitHub Actions has run successfully.

## Outstanding checks

- Docker and uv were not found in the initial development environment's PATH. PostgreSQL and Compose integration have not been executed.
- The PDF extraction path is implemented but has not been tested with a PDF fixture. OCR is not supported.
- The GitHub Actions workflow is prepared; no remote workflow result has been verified.
- Python 3.12 CI compatibility and the container build require separate verification.
- Semantic embeddings, broader answer-quality evaluation, and fairness evaluation remain outstanding.

`requirements-snapshot.txt` records the dependency resolution from the initial Python 3.14 environment. It is an environment snapshot, not a cross-platform lockfile.
