import logging

from agents.llm import llm

logger = logging.getLogger(__name__)


def planner_agent(query: str) -> str:
    """Break down a user query into retrieval-focused steps."""
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
    plan = llm.invoke(prompt)
    logger.info(f"Plan generated: {plan[:100]}...")
    return plan
