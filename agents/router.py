import logging

from agents.llm import llm
from config import settings

logger = logging.getLogger(__name__)

QUERY_TYPES = ["factual", "comparative", "summarization", "out_of_scope"]

STRATEGIES = {
    "factual": {"k_multiplier": 1, "context_limit": settings.context_max_chars},
    "comparative": {"k_multiplier": 2, "context_limit": settings.context_max_chars * 2},
    "summarization": {"k_multiplier": 3, "context_limit": settings.context_max_chars * 2},
    "out_of_scope": {"k_multiplier": 0, "context_limit": 0},
}


def router_agent(query: str) -> dict:
    """Classify the query type and determine retrieval strategy.

    Returns:
        dict with keys: query_type (str), strategy (dict)
    """
    prompt = f"""You are a query classifier for a medical RAG system.
Classify the following query into exactly one category:
- factual: specific medical fact lookup (symptoms, treatments, definitions)
- comparative: comparing conditions, treatments, or approaches
- summarization: requesting an overview or summary of a topic
- out_of_scope: not related to healthcare or medicine

Query: {query}

Respond with ONLY the category name, nothing else."""

    try:
        classification = llm.invoke(prompt).strip().lower()

        # Clean up LLM response — extract just the category
        for qt in QUERY_TYPES:
            if qt in classification:
                classification = qt
                break
        else:
            classification = "factual"

    except Exception as e:
        logger.warning(f"Router failed, defaulting to factual: {e}")
        classification = "factual"

    strategy = STRATEGIES.get(classification, STRATEGIES["factual"])
    logger.info(f"Query classified as: {classification}")

    return {
        "query_type": classification,
        "strategy": strategy,
    }
