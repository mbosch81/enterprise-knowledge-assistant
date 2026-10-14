"""Deterministic offline baseline. No LLM or semantic model is implied."""
import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import Path

DIM = 256

def tokens(text):
    return re.findall(r"[a-zäöüß0-9]+", text.lower())

def embed(text):
    vector = [0.0] * DIM
    for token in tokens(text):
        vector[int.from_bytes(hashlib.sha256(token.encode()).digest()[:4], "big") % DIM] += 1
    norm = math.sqrt(sum(x*x for x in vector)) or 1
    return [x/norm for x in vector]

@dataclass(frozen=True)
class Chunk:
    id: str
    tenant: str
    source: str
    location: str
    text: str

def ingest(path: Path, tenant: str):
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        parts = [(f"page:{i+1}", p.extract_text() or "") for i,p in enumerate(PdfReader(path).pages)]
    elif path.suffix.lower() == ".md":
        parts = [("markdown", path.read_text(encoding="utf-8"))]
    else:
        raise ValueError("Only Markdown and text PDFs are supported")
    result = []
    for location, text in parts:
        words = text.split()
        for start in range(0, len(words), 100):
            content = " ".join(words[start:start+120])
            identity = f"{tenant}:{path.name}:{location}:{start}:{content}"
            result.append(Chunk(hashlib.sha256(identity.encode()).hexdigest(), tenant, path.name, f"{location}:word:{start}", content))
    return result

class MemoryStore:
    def __init__(self):
        self.chunks = {}
    def upsert(self, chunks):
        for c in chunks:
            self.chunks[c.id] = c
    def search(self, tenant, question, limit=3):
        q = embed(question)
        matches = [(sum(a*b for a,b in zip(q, embed(c.text))), c) for c in self.chunks.values() if c.tenant == tenant]
        return sorted(matches, key=lambda pair: (-pair[0], pair[1].id))[:limit]

def answer(store, tenant, question):
    matches = store.search(tenant, question)
    # Conservative lexical evidence gate; a similarity score alone is insufficient.
    stop = {"the", "is", "what", "how", "a", "are", "does", "for", "of", "in", "to"}
    query = set(tokens(question)) - stop
    citations = []
    for score, chunk in matches:
        if re.search(r"ignore .*instructions|reveal secrets|system prompt", chunk.text, re.I):
            continue  # Narrow demonstrative quarantine, not a complete injection defense.
        for sentence in re.split(r"(?<=[.!?]) +", chunk.text):
            overlap = query & set(tokens(sentence))
            if score >= 0.12 and len(overlap) >= min(2, len(query)) and query:
                citations.append({"chunk_id": chunk.id, "source": chunk.source, "location": chunk.location, "quote": sentence})
    return {"answer": " ".join(c["quote"] for c in citations[:2]) if citations else "I do not know based on the available evidence.", "abstained": not citations, "citations": citations[:2], "provider": "offline-extractive-v1", "model_tokens": 0, "model_cost_usd": 0}
