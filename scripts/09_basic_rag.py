import chromadb

from src.embeddings import (
    create_embedding
)

from src.rag_prompt import (
    build_rag_prompt
)

from src.generator import (
    generate_answer
)


# --------------------------------------------------
# CONNECT TO VECTOR DATABASE
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)


collection = client.get_collection(
    name="novatech_knowledge"
)


# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

# Step 9.4: swap in the cross-document question to test
# Product Specification + Integration Guide evidence:
#
# question = """
# Which NovaTech product can integrate with Siemens SCADA
# and provide advanced predictive maintenance?
# """

question = """
Which product is suitable for predictive maintenance
of industrial motors?
"""


print("QUESTION")
print("-" * 60)
print(question.strip())


# --------------------------------------------------
# EMBED QUESTION
# --------------------------------------------------

query_embedding = create_embedding(
    question
)


# --------------------------------------------------
# RETRIEVE
# --------------------------------------------------

results = collection.query(
    query_embeddings=[
        query_embedding
    ],
    n_results=5,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)


documents = results["documents"]
metadatas = results["metadatas"]
distances = results["distances"]


assert documents is not None
assert metadatas is not None
assert distances is not None


retrieved_chunks = []


for document, metadata, distance in zip(
    documents[0],
    metadatas[0],
    distances[0]
):

    retrieved_chunks.append({
        "text": document,
        "source": metadata["filename"],
        "distance": distance
    })


# --------------------------------------------------
# SHOW RETRIEVAL
# --------------------------------------------------

print("\nRETRIEVED SOURCES")
print("-" * 60)


for i, chunk in enumerate(
    retrieved_chunks,
    start=1
):

    print(
        f"{i}. {chunk['source']} "
        f"(distance={chunk['distance']:.4f})"
    )


# --------------------------------------------------
# AUGMENT
# --------------------------------------------------

prompt = build_rag_prompt(
    question,
    retrieved_chunks
)


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

answer = generate_answer(
    prompt
)


print("\nANSWER")
print("=" * 60)

print(answer)
