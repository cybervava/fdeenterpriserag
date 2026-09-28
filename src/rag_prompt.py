def build_rag_prompt(
    question,
    retrieved_chunks
):

    """Build a grounded prompt using retrieved enterprise knowledge."""

    context_parts = []

    for i, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {i}
Document: {chunk['source']}

{chunk['text']}
"""
        )

    context = "\n".join(
        context_parts
    )

    prompt = f"""
You are the NovaTech Enterprise Product Intelligence Assistant.

Answer the user's question using ONLY the enterprise
context provided below.

Rules:
1. Do not invent product capabilities.
2. Base your answer only on the provided context.
3. Cite supporting information using [Source 1],
   [Source 2], etc.
4. If the context does not contain enough information,
   say: "The available enterprise knowledge does not
   contain enough information to answer this question."

ENTERPRISE CONTEXT

{context}

USER QUESTION

{question}

ANSWER
"""

    return prompt
