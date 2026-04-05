from agents.llm import llm


def evaluator_agent(query: str, context: str, answer: str) -> str:
    prompt = f"""
You are an AI evaluator.

Evaluate the answer based ONLY on the context.

Check:
1. Is the answer supported by the context?
2. Is it relevant to the question?
3. Is there any hallucination?

Context:
{context}

Question:
{query}

Answer:
{answer}

Respond in this exact format:
Score: (0-10)
Verdict: (GOOD / BAD)
Feedback: (short explanation)
"""
    return llm.invoke(prompt)