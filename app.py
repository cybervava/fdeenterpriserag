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
# RETRIEVAL
# --------------------------------------------------

def retrieve_chunks(
    question,
    top_k=5
):

    query_embedding = create_embedding(
        question
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
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

    return retrieved_chunks


# --------------------------------------------------
# COMPLETE RAG PIPELINE
# --------------------------------------------------

def ask_rag(question):

    retrieved_chunks = retrieve_chunks(
        question,
        top_k=5
    )

    prompt = build_rag_prompt(
        question,
        retrieved_chunks
    )

    answer = generate_answer(
        prompt
    )

    return answer, retrieved_chunks


# --------------------------------------------------
# INTERACTIVE APPLICATION
# --------------------------------------------------

print("=" * 65)

print(
    "NOVATECH ENTERPRISE PRODUCT INTELLIGENCE ASSISTANT"
)

print("=" * 65)

print(
    "\nAsk questions about NovaTech products and solutions."
)

print(
    "Type 'exit' or 'quit' to stop."
)


while True:

    question = input(
        "\nQuestion: "
    ).strip()

    if question.lower() in [
        "exit",
        "quit"
    ]:

        print(
            "\nRAG application stopped."
        )

        break

    if not question:
        continue

    try:

        print(
            "\nSearching enterprise knowledge..."
        )

        answer, sources = ask_rag(
            question
        )

        print("\nANSWER")
        print("-" * 65)

        print(answer)

        print("\nRETRIEVED SOURCES")
        print("-" * 65)

        for i, source in enumerate(
            sources,
            start=1
        ):

            print(
                f"{i}. "
                f"{source['source']} "
                f"(distance="
                f"{source['distance']:.4f})"
            )

    except Exception as error:

        print(
            "\nError:",
            error
        )
