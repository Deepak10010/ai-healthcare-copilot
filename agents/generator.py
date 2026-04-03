from langchain_community.llms import Ollama

def generator_agent(query, context):
    llm = Ollama(model="llama3")

    prompt = f"""
    You are a medical assistant.

    Use ONLY the provided context to answer the question.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question:
    {query}

    Answer clearly:
    """

    response = llm.invoke(prompt)

    return response