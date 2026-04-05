from agents.llm import llm


def planner_agent(query: str) -> str:
    prompt = f"""
You are a planning agent for a RAG system.

ONLY break down the user query into simple retrieval-focused steps.
DO NOT add external knowledge.
DO NOT assume facts not in the query.
Keep it short and relevant.

Query:
{query}

Steps:
"""
    return llm.invoke(prompt)