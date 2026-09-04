"""The embedder under test.

CONNECTOME v5.5 section 5.1.  Which embedder serves a corpus is decided by the loss -
the one whose field predicts that corpus's own future best - not by a leaderboard.  The
exact instruction string is part of the model's identity: a changed instruction is a
silent model swap, so it is recorded with every run.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

import numpy as np

# Qwen3-Embedding's card: the instruction goes on the query side only, never on the
# document side.  Measured on the estate: +3.5 points recall@10 (n=28 free goldens).
QUERY_INSTRUCTION = (
    "Instruct: Given a passage from a working corpus, retrieve the passages it refers to\nQuery:"
)


@dataclass(frozen=True)
class Embedder:
    endpoint: str = "http://127.0.0.1:8092/v1/embeddings"
    model: str = ""
    query_instruction: str = ""     # "" means the document side: no instruction
    batch: int = 8
    timeout: float = 180.0

    def fingerprint(self) -> str:
        """What a stored vector must be tagged with to be comparable later."""
        return json.dumps(
            {"endpoint": self.endpoint, "model": self.model, "instruction": self.query_instruction},
            sort_keys=True,
        )

    def encode(self, texts: list[str]) -> np.ndarray:
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch):
            chunk = [self.query_instruction + t for t in texts[i : i + self.batch]]
            payload = {"input": chunk}
            if self.model:
                payload["model"] = self.model
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as fh:
                body = json.loads(fh.read())
            out.extend(item["embedding"] for item in body["data"])
        arr = np.asarray(out, dtype=np.float32)
        arr /= np.linalg.norm(arr, axis=1, keepdims=True) + 1e-9
        return arr


def server_model(endpoint: str = "http://127.0.0.1:8092/v1/models") -> str | None:
    """Which model the local server is actually serving, or None if it is down."""
    try:
        with urllib.request.urlopen(endpoint, timeout=5) as fh:
            body = json.loads(fh.read())
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    data = body.get("data") or body.get("models") or []
    if not data:
        return None
    first = data[0]
    return first.get("id") or first.get("name")
