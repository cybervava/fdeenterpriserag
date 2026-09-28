import chromadb

from src.document_loader import (
    load_documents
)

from src.text_cleaner import (
    clean_text
)

from src.chunker import (
    chunk_text
)

from src.embeddings import (
    create_embeddings
)


# --------------------------------------------------
# LOAD DOCUMENTS
# --------------------------------------------------

documents = load_documents(
    "data/knowledge_base"
)

print(
    "Documents loaded:",
    len(documents)
)


# --------------------------------------------------
# CLEAN AND CHUNK
# --------------------------------------------------

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
    "Chunks created:",
    len(all_chunks)
)


# --------------------------------------------------
# CREATE PERSISTENT CHROMA DATABASE
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)


COLLECTION_NAME = (
    "novatech_knowledge"
)


# Delete old development collection
# so rerunning does not create duplicates.

try:
    client.delete_collection(
        name=COLLECTION_NAME
    )

except Exception:
    pass


collection = client.create_collection(
    name=COLLECTION_NAME
)


# --------------------------------------------------
# EMBED AND STORE IN BATCHES
# --------------------------------------------------

BATCH_SIZE = 100


for start in range(
    0,
    len(all_chunks),
    BATCH_SIZE
):

    batch = all_chunks[
        start:start + BATCH_SIZE
    ]

    texts = [
        item["text"]
        for item in batch
    ]

    embeddings = create_embeddings(
        texts
    )

    ids = [
        f"chunk_{start + i}"
        for i in range(len(batch))
    ]

    metadatas = [
        {
            "filename":
                item["filename"],

            "source":
                item["source"],

            "chunk_number":
                item["chunk_number"]
        }

        for item in batch
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,  # type: ignore[arg-type]
        metadatas=metadatas
    )

    stored = min(
        start + BATCH_SIZE,
        len(all_chunks)
    )

    print(
        f"Stored {stored}/{len(all_chunks)} chunks"
    )


# --------------------------------------------------
# VERIFY
# --------------------------------------------------

print("\nVECTOR DATABASE CREATED")

print(
    "Vectors stored:",
    collection.count()
)
