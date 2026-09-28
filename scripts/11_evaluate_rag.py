import chromadb

from src.embeddings import (
    create_embedding
)

from tests.evaluation_questions import (
    EVALUATION_QUESTIONS
)


# --------------------------------------------------
# CONNECT TO DATABASE
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)


collection = client.get_collection(
    name="novatech_knowledge"
)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

passed = 0

total = len(
    EVALUATION_QUESTIONS
)


print("=" * 65)
print("BASELINE RAG RETRIEVAL EVALUATION")
print("=" * 65)


for number, test in enumerate(
    EVALUATION_QUESTIONS,
    start=1
):

    question = test["question"]

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
            "metadatas"
        ]
    )

    metadatas = results[
        "metadatas"
    ]

    assert metadatas is not None

    retrieved_sources = [
        metadata["filename"]
        for metadata in metadatas[0]
    ]

    success = False

    if "expected_source" in test:

        success = (
            test["expected_source"]
            in retrieved_sources
        )

    elif "expected_source_contains" in test:

        expected_text = test[
            "expected_source_contains"
        ]

        success = any(
            expected_text in source
            for source in retrieved_sources
        )

    if success:
        passed += 1

    status = (
        "PASS"
        if success
        else "FAIL"
    )

    print(
        f"\nTest {number}: {status}"
    )

    print(
        "Question:",
        question
    )

    print(
        "Retrieved sources:"
    )

    for rank, source in enumerate(
        retrieved_sources,
        start=1
    ):

        print(
            f" {rank}. {source}"
        )


# --------------------------------------------------
# FINAL SCORE
# --------------------------------------------------

accuracy = (
    passed / total * 100
)


print("\n" + "=" * 65)

print(
    f"Passed: {passed}/{total}"
)

print(
    f"Retrieval Accuracy: "
    f"{accuracy:.1f}%"
)

print("=" * 65)
