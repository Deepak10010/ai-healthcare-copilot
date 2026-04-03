from langchain_community.llms import Ollama


def evaluator_agent(query, context, answer):
    llm = Ollama(model="llama3")

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

    Respond in this format:
    Score: (0-10)
    Verdict: (GOOD / BAD)
    Feedback: (short explanation)
    """

    evaluation = llm.invoke(prompt)

    return evaluation