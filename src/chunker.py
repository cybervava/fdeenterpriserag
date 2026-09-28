def chunk_text(
    text,
    chunk_size=300,
    overlap=50
):

    # Guard: the window must advance, otherwise the loop never ends.
    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks
