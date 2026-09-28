import os
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def create_embedding(text):
    """Generate an embedding for a single text."""

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return np.array(
        response.data[0].embedding,
        dtype=np.float32
    )


def create_embeddings(texts):
    """Generate embeddings for multiple texts."""

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [
        np.array(
            item.embedding,
            dtype=np.float32
        )
        for item in response.data
    ]
