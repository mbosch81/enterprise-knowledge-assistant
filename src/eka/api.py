import json
import logging
import os
import secrets
import time
import uuid
import urllib.error
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from eka.core import MemoryStore, ingest
# This project never exports prompt/document content through inherited tracing settings.
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"
from eka.agent import build_agent

logger = logging.getLogger("eka.metrics")
security = HTTPBearer()

class Question(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    model_config = {"extra": "forbid"}

def create_app(store=None, credentials=None):
    if store is None:
        dsn = os.getenv("DATABASE_URL")
        if dsn:
            from eka.postgres import PostgresStore
            store = PostgresStore(dsn)
        else:
            store = MemoryStore()
        for path in sorted(Path("data/synthetic").glob("*.md")):
            store.upsert(ingest(path, "demo"))
    credentials = credentials if credentials is not None else json.loads(os.getenv("EKA_TOKENS", "{}"))
    if not credentials:
        raise RuntimeError('Set EKA_TOKENS to a JSON mapping of secret bearer tokens to tenants')
    app = FastAPI(title="Enterprise Knowledge Assistant", version="0.1.0")
    provider = None
    if os.getenv("EKA_PROVIDER", "offline") == "ollama":
        from eka.ollama import OllamaProvider
        model = os.environ["OLLAMA_MODEL"]
        provider = OllamaProvider(os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"), model, timeout=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90")))
    agent = build_agent(store, provider)
    def principal(auth: HTTPAuthorizationCredentials = Depends(security)):
        for token, tenant in credentials.items():
            if secrets.compare_digest(token, auth.credentials):
                return tenant
        raise HTTPException(status_code=401, detail="Invalid credentials")
    @app.get("/health")
    def health():
        return {"status": "ok", "provider": "offline-extractive-v1"}
    @app.post("/ask")
    def ask(body: Question, tenant=Depends(principal)):
        start = time.perf_counter()
        try:
            result = agent.invoke({"tenant": tenant, "question": body.question}, config={"recursion_limit": 4})["result"]
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
            raise HTTPException(status_code=503, detail="Model unavailable or evidence validation failed") from None
        result["latency_ms"] = round((time.perf_counter()-start)*1000, 3)
        result["request_id"] = str(uuid.uuid4())
        logger.info(json.dumps({k: result[k] for k in ("request_id", "latency_ms", "abstained", "provider", "model_tokens", "model_cost_usd")}))
        return result
    return app
