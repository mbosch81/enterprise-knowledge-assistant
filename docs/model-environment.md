# Model environment configuration

## Offline baseline

Set `EKA_PROVIDER=offline` to run deterministic tests and the demo without a model server or paid API calls.

## Local Ollama inference

Set `EKA_PROVIDER=ollama`, `OLLAMA_URL` to a reachable Ollama server, and `OLLAMA_MODEL` to an installed text model. Keep environment-specific addresses and real credentials in your ignored local `.env`.

For a server running on the same machine, a host process can use `http://127.0.0.1:11434`. A Docker Desktop container can reach a server on the host through `http://host.docker.internal:11434`. For a remote server, configure its address explicitly. Check available models through `/api/tags` before choosing one.

The application uses `/api/generate` with structured JSON output. `OLLAMA_TIMEOUT_SECONDS` defaults to 90 seconds and controls the socket timeout, not a hard end-to-end deadline. The verified development run used `qwen3:14b` on a remote local-network GPU server; see [verification](verification.md).

Export variables explicitly when starting the API on the host: the application does not automatically load `.env`. Docker Compose reads `.env` for interpolation and passes configured variables to the container.

## Optional gateways and cloud providers

A shared gateway may automatically fall back from local inference to a cloud API. This can transfer questions and evidence outside the local environment and incur charges. Configure such a gateway only after explicitly choosing that behavior and its budget. The demonstrated local run used a direct GPU endpoint and made no cloud request.

Gateway support for structured output, token accounting, and `/api/embed` must be checked separately. Availability of a generation model does not establish suitability for semantic embeddings. Dedicated embedding integration is still planned.

No infrastructure changes or copied provider credentials are required for this project configuration.
