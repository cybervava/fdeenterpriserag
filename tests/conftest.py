import hashlib
import os
import re
from types import SimpleNamespace

import numpy as np
import pytest

# src.embeddings / src.generator build an OpenAI client at import time,
# which raises without a key. Tests never hit the network.
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")

EMBEDDING_DIMENSIONS = 1536


def fake_vector(text):
    """Deterministic hashed bag-of-words vector (stand-in for OpenAI embeddings)."""
    vector = np.zeros(EMBEDDING_DIMENSIONS, dtype=np.float32)
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        index = int(hashlib.md5(token.encode()).hexdigest(), 16) % EMBEDDING_DIMENSIONS
        vector[index] += 1.0
    norm = np.linalg.norm(vector)
    return (vector / norm if norm else vector).tolist()


class FakeEmbeddings:
    def __init__(self):
        self.calls = []

    def create(self, model, input):
        self.calls.append({"model": model, "input": input})
        texts = [input] if isinstance(input, str) else input
        return SimpleNamespace(
            data=[SimpleNamespace(embedding=fake_vector(text)) for text in texts]
        )


class FakeResponses:
    def __init__(self):
        self.calls = []

    def create(self, model, input):
        self.calls.append({"model": model, "input": input})
        if "trigger-error" in input:
            raise RuntimeError("simulated OpenAI failure")
        return SimpleNamespace(output_text="Fake grounded answer [Source 1]")


class FakeOpenAIClient:
    def __init__(self):
        self.embeddings = FakeEmbeddings()
        self.responses = FakeResponses()


@pytest.fixture
def fake_client(monkeypatch):
    import src.embeddings
    import src.generator

    client = FakeOpenAIClient()
    monkeypatch.setattr(src.embeddings, "client", client)
    monkeypatch.setattr(src.generator, "client", client)
    return client
