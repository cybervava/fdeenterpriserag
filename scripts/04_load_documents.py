from src.document_loader import (
    load_documents
)


documents = load_documents(
    "data/knowledge_base"
)


print(
    "Documents loaded:",
    len(documents)
)


print("\nSample document")
print("-" * 60)

print(
    "Filename:",
    documents[0]["filename"]
)

print(
    "Source:",
    documents[0]["source"]
)

print("\nContent:")

print(
    documents[0]["text"][:500]
)
