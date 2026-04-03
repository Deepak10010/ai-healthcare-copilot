from langchain_community.llms import Ollama

def planner_agent(query):
    llm = Ollama(model="llama3")

    prompt = f"""
    You are a planning agent for a RAG system.

    ONLY break down the user query into steps.
    DO NOT add external knowledge.
    DO NOT assume facts not in the query.

    Keep it simple and relevant to retrieval.

    Query:
    {query}

    Steps:
    """

    response = llm.invoke(prompt)

    return response