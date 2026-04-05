from agents.llm import llm


def generator_agent(query: str, context: str) -> str:
    prompt = f"""
You are a medical assistant.

Use ONLY the provided context to answer the question.
If the answer is not in the context, say exactly:
"I don't know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
    return llm.invoke(prompt)