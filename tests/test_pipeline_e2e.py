"""Runs every lab script end-to-end in an isolated directory.

OpenAI is replaced by the deterministic fake client from conftest, so this
proves the plumbing (dataset -> chunks -> ChromaDB -> retrieval -> prompt ->
answer -> evaluation), not the real baseline retrieval score.
"""
import builtins
import runpy
from pathlib import Path

import chromadb
import pytest

from tests.evaluation_questions import EVALUATION_QUESTIONS

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_script(relative_path):
    runpy.run_path(str(PROJECT_ROOT / relative_path), run_name="__main__")


@pytest.fixture
def workspace(tmp_path, monkeypatch, fake_client):
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    monkeypatch.chdir(tmp_path)
    yield tmp_path
    chromadb.api.client.SharedSystemClient.clear_system_cache()


def test_full_lab_pipeline(workspace, fake_client, monkeypatch, capsys):
    run_script("scripts/00_environment_test.py")
    assert "Python environment is working." in capsys.readouterr().out

    monkeypatch.setattr("openai.OpenAI", lambda **_kwargs: fake_client)
    run_script("scripts/01_test_openai.py")
    assert "Fake grounded answer" in capsys.readouterr().out
    assert fake_client.responses.calls[-1]["model"] == "gpt-5-mini"

    run_script("scripts/02_generate_dataset.py")
    out = capsys.readouterr().out
    assert "Total documents: 294" in out
    assert len(list((workspace / "data/knowledge_base").rglob("*.txt"))) == 294

    run_script("scripts/03_inspect_dataset.py")
    assert "Total documents: 294" in capsys.readouterr().out

    run_script("scripts/04_load_documents.py")
    assert "Documents loaded: 294" in capsys.readouterr().out

    run_script("scripts/05_clean_and_chunk.py")
    assert "Chunks created: 294" in capsys.readouterr().out

    run_script("scripts/06_test_embeddings.py")
    assert "Embedding dimensions: 1536" in capsys.readouterr().out

    run_script("scripts/07_build_vector_db.py")
    out = capsys.readouterr().out
    for line in ["Stored 100/294 chunks", "Stored 200/294 chunks",
                 "Stored 294/294 chunks", "Vectors stored: 294"]:
        assert line in out

    # Rebuilding must replace the collection, not duplicate it.
    run_script("scripts/07_build_vector_db.py")
    assert "Vectors stored: 294" in capsys.readouterr().out

    run_script("scripts/08_test_retrieval.py")
    out = capsys.readouterr().out
    assert out.count("RESULT ") == 5
    assert "Distance:" in out

    run_script("scripts/09_basic_rag.py")
    out = capsys.readouterr().out
    assert "RETRIEVED SOURCES" in out
    assert "Fake grounded answer [Source 1]" in out
    last_prompt = fake_client.responses.calls[-1]["input"]
    assert last_prompt.count("SOURCE ") == 5
    assert "predictive maintenance" in last_prompt

    run_script("scripts/11_evaluate_rag.py")
    out = capsys.readouterr().out
    assert out.count("Test ") == len(EVALUATION_QUESTIONS)
    assert f"/{len(EVALUATION_QUESTIONS)}" in out
    assert "Retrieval Accuracy:" in out

    answers = iter(["", "Which products support MQTT?", "trigger-error please", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(answers))
    run_script("app.py")
    out = capsys.readouterr().out
    assert "NOVATECH ENTERPRISE PRODUCT INTELLIGENCE ASSISTANT" in out
    assert "Fake grounded answer [Source 1]" in out
    assert out.count("(distance=") == 5
    assert "Error: simulated OpenAI failure" in out
    assert "RAG application stopped." in out
