from src.document_loader import (
    load_documents
)

from src.text_cleaner import (
    clean_text
)

from src.chunker import (
    chunk_text
)


documents = load_documents(
    "data/knowledge_base"
)


all_chunks = []


for document in documents:

    cleaned_text = clean_text(
        document["text"]
    )

    chunks = chunk_text(
        cleaned_text,
        chunk_size=300,
        overlap=50
    )

    for chunk_number, chunk in enumerate(
        chunks
    ):

        all_chunks.append({
            "text": chunk,
            "filename": document["filename"],
            "source": document["source"],
            "chunk_number": chunk_number
        })

print(
    "Documents loaded:",
    len(documents)
)

print(
    "Chunks created:",
    len(all_chunks)
)


print("\nSample chunk")
print("-" * 60)

print(
    "Source:",
    all_chunks[0]["filename"]
)

print(
    "Chunk number:",
    all_chunks[0]["chunk_number"]
)

print("\nContent:")

print(
    all_chunks[0]["text"]
)
