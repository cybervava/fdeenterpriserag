import numpy as np

from src.embeddings import create_embedding, create_embeddings
from src.generator import generate_answer


def test_create_embedding_returns_float32_vector(fake_client):
    vector = create_embedding("NovaSense X500")

    assert isinstance(vector, np.ndarray)
    assert vector.dtype == np.float32
    assert vector.shape == (1536,)
    assert fake_client.embeddings.calls == [
        {"model": "text-embedding-3-small", "input": "NovaSense X500"}
    ]


def test_create_embeddings_returns_one_vector_per_text(fake_client):
    vectors = create_embeddings(["a", "b", "c"])

    assert len(vectors) == 3
    assert all(v.dtype == np.float32 and v.shape == (1536,) for v in vectors)
    assert fake_client.embeddings.calls[0]["input"] == ["a", "b", "c"]


def test_generate_answer_uses_gpt5_mini_and_returns_output_text(fake_client):
    answer = generate_answer("prompt text")

    assert answer == "Fake grounded answer [Source 1]"
    assert fake_client.responses.calls == [
        {"model": "gpt-5-mini", "input": "prompt text"}
    ]
