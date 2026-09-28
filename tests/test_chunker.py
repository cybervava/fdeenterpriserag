import pytest

from src.chunker import chunk_text


def words(n):
    return " ".join(f"w{i}" for i in range(n))


def test_short_text_produces_single_chunk():
    assert chunk_text(words(10)) == [words(10)]


def test_empty_text_produces_no_chunks():
    assert chunk_text("") == []


def test_chunks_respect_size_and_overlap():
    chunks = chunk_text(words(10), chunk_size=4, overlap=1)

    assert chunks == [
        "w0 w1 w2 w3",
        "w3 w4 w5 w6",
        "w6 w7 w8 w9",
        "w9",
    ]


def test_baseline_config_on_long_text():
    chunks = chunk_text(words(600), chunk_size=300, overlap=50)

    assert len(chunks) == 3
    assert chunks[0].split()[-50:] == chunks[1].split()[:50]
    assert all(len(chunk.split()) <= 300 for chunk in chunks)


@pytest.mark.parametrize("overlap", [4, 5])
def test_rejects_overlap_not_smaller_than_chunk_size(overlap):
    with pytest.raises(ValueError):
        chunk_text(words(10), chunk_size=4, overlap=overlap)
