import chromadb

from src.embeddings import (
    create_embedding
)


client = chromadb.PersistentClient(
    path="chroma_db"
)


collection = client.get_collection(
    name="novatech_knowledge"
)


question = """
Which product is suitable for predictive maintenance
of industrial motors?
"""


print("QUESTION")
print("-" * 60)
print(question.strip())


query_embedding = create_embedding(
    question
)


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


print("\nRETRIEVED RESULTS")
print("=" * 60)


for i, (
    document,
    metadata,
    distance
) in enumerate(
    zip(
        documents[0],
        metadatas[0],
        distances[0]
    ),
    start=1
):

    print(
        f"\nRESULT {i}"
    )

    print(
        "Source:",
        metadata["filename"]
    )

    print(
        "Distance:",
        round(distance, 4)
    )

    print("\nContent:")
    print(document)

    print("-" * 60)
