from langchain_community.llms import Ollama

def planner_agent(query):
    llm = Ollama(model="llama3")

    prompt = f"""
    You are an intelligent AI planner.

    Break the user query into clear steps needed to answer it.

    Keep steps simple and structured.

    Query:
    {query}

    Steps:
    """

    response = llm.invoke(prompt)

    return response