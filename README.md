# Enterprise RAG from Scratch — NovaTech Product Intelligence Assistant

Baseline RAG v1 built step by step (Steps 1–11 of the student lab guide) with
Python, OpenAI (`text-embedding-3-small` + `gpt-5-mini`) and ChromaDB, over a
synthetic 294-document knowledge base for the fictional company
NovaTech Industrial Solutions.

```
Enterprise Documents → Load → Clean → Chunk (300 words / 50 overlap)
  → Embeddings (1536-d) → ChromaDB (persistent) → Top-5 Semantic Retrieval
  → Grounded RAG Prompt → gpt-5-mini → Interactive App → Baseline Evaluation (Hit@5)
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then set OPENAI_API_KEY
```

Run every command from the project root with `PYTHONPATH=.` so scripts can import `src/`.

## Lab steps

| Step | Command | Expected |
|------|---------|----------|
| 1  | `PYTHONPATH=. python scripts/00_environment_test.py` | Your `.venv` Python executable |
| 2  | `PYTHONPATH=. python scripts/01_test_openai.py` | Two-sentence answer from gpt-5-mini |
| 3  | `PYTHONPATH=. python scripts/02_generate_dataset.py` | `Total documents: 294` |
| 3A | `PYTHONPATH=. python scripts/03_inspect_dataset.py` | Counts per category + sample doc |
| 4  | `PYTHONPATH=. python scripts/04_load_documents.py` | `Documents loaded: 294` |
| 5  | `PYTHONPATH=. python scripts/05_clean_and_chunk.py` | `Chunks created: 294` |
| 6  | `PYTHONPATH=. python scripts/06_test_embeddings.py` | `Embedding dimensions: 1536` |
| 7  | `PYTHONPATH=. python scripts/07_build_vector_db.py` | `Vectors stored: 294`, creates `chroma_db/` |
| 8  | `PYTHONPATH=. python scripts/08_test_retrieval.py` | Top-5 chunks with distances |
| 9  | `PYTHONPATH=. python scripts/09_basic_rag.py` | Retrieved sources + cited answer |
| 10 | `PYTHONPATH=. python app.py` | Interactive Q&A loop (`exit` / `quit` to stop) |
| 11 | `PYTHONPATH=. python scripts/11_evaluate_rag.py` | PASS/FAIL per question + Retrieval Accuracy |

The knowledge base in `data/knowledge_base/` is committed (generated with `random.seed(42)`),
so Step 3 is only needed to regenerate it. `chroma_db/` and `.env` are git-ignored.

### Questions to try in the app (Steps 10–11.5)

- Which product is suitable for predictive maintenance of industrial motors?
- Which products support MQTT?
- Can the X500 integrate with Siemens SCADA?
- What is the operating temperature of the X500? → `-20°C to 90°C`
- What is the warranty period for the NovaSense X500? → should **abstain**

Judge generation on **correctness**, **groundedness** and **abstention**.

## Baseline evaluation

`tests/evaluation_questions.py` holds five ground-truth questions. The metric is Hit@5:
does the expected source appear anywhere in the Top-5 retrieved chunks? Record the score you
actually get — failures are the input to the optimization phase (Step 12+), which should change
one thing at a time and re-run this same evaluation.

## Tests

```bash
python -m pytest --cov --cov-report=term-missing
```

Unit tests cover the loader, cleaner, chunker, prompt builder and OpenAI wrappers.
`tests/test_pipeline_e2e.py` runs every lab script and `app.py` end-to-end in a temp directory
against a real ChromaDB, with OpenAI replaced by a deterministic fake client — so it needs no API
key and verifies the plumbing, not the real retrieval score.

## Layout

```
app.py                     Step 10 interactive RAG app
data/knowledge_base/       294 synthetic documents in 7 categories
scripts/00–11_*.py         One script per lab step
src/
  document_loader.py       Load *.txt → {text, filename, source}
  text_cleaner.py          Normalize line endings / whitespace
  chunker.py               Word-window chunking (300 / 50)
  embeddings.py            text-embedding-3-small (single + batch)
  rag_prompt.py            Grounded prompt with [Source N] citations + abstention rule
  generator.py             gpt-5-mini via the Responses API
tests/
  evaluation_questions.py  Ground-truth set for Step 11
  test_*.py                pytest suite
```
