from src.embeddings import (
    create_embedding
)


text = """
NovaSense X500 provides predictive maintenance
for industrial motors and rotating equipment.
"""


embedding = create_embedding(
    text
)


print(
    "Embedding dimensions:",
    len(embedding)
)

print(
    "\nFirst 10 values:"
)

print(
    embedding[:10]
)
