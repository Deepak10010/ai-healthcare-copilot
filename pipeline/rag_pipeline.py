import logging
import re

from agents.planner import planner_agent
from agents.retriever import retriever_agent
from agents.generator import generator_agent
from agents.evaluator import evaluator_agent
from config import settings
from logging_config import PipelineTimer

logger = logging.getLogger(__name__)


def parse_evaluation_score(evaluation: str) -> int:
    """Extract the numeric score from evaluator output."""
    match = re.search(r"Score:\s*(\d+)", evaluation)
    if match:
        return int(match.group(1))
    return 0


def ask_question_agentic(
    db, query: str, max_retries: int = None, session_id: str = None
) -> dict:
    """Run the full RAG pipeline: route -> plan -> retrieve -> generate -> evaluate.

    Returns:
        dict with keys: answer, sources, evaluation, query_type, plan, timing
    """
    max_retries = max_retries if max_retries is not None else settings.max_retries
    timings = {}

    # --- Step 0: Query Routing ---
    query_type = "factual"
    strategy = None
    if settings.router_enabled:
        with PipelineTimer("Router Agent", logger) as t:
            from agents.router import router_agent

            routing = router_agent(query)
            query_type = routing["query_type"]
            strategy = routing["strategy"]
        timings["router"] = t.elapsed

        if query_type == "out_of_scope":
            logger.info("Query classified as out-of-scope, skipping retrieval")
            return {
                "answer": "This question appears to be outside the scope of the medical documents available. Please ask a healthcare-related question.",
                "sources": [],
                "evaluation": "N/A - out of scope",
                "query_type": query_type,
                "plan": "N/A",
                "timing": timings,
            }

    # --- Step 1: Planner Agent ---
    with PipelineTimer("Planner Agent", logger) as t:
        plan = planner_agent(query)
    timings["planner"] = t.elapsed

    # --- Step 2: Retriever Agent ---
    with PipelineTimer("Retriever Agent", logger) as t:
        retrieval_result = retriever_agent(db, query, strategy=strategy)
        context = retrieval_result["context"]
        sources = retrieval_result["sources"]
    timings["retriever"] = t.elapsed

    # --- Step 3: Get conversation history ---
    chat_history = ""
    if session_id:
        from memory.conversation import conversation_store

        conversation_store.add_message(session_id, "user", query)
        chat_history = conversation_store.format_history_for_prompt(session_id)

    # --- Step 4: Generator + Evaluator Loop ---
    attempt = 0
    answer = ""
    evaluation = ""

    while attempt <= max_retries:
        logger.info(f"Generation attempt {attempt + 1}/{max_retries + 1}")

        with PipelineTimer(f"Generator Agent (attempt {attempt + 1})", logger) as t:
            answer = generator_agent(query, context, chat_history=chat_history)
        timings[f"generator_attempt_{attempt + 1}"] = t.elapsed

        with PipelineTimer("Evaluator Agent", logger) as t:
            evaluation = evaluator_agent(query, context, answer)
        timings["evaluator"] = t.elapsed

        if "GOOD" in evaluation.upper():
            logger.info("Answer accepted by evaluator")
            break

        logger.warning(f"Answer rejected (attempt {attempt + 1}), retrying...")
        attempt += 1

    if attempt > max_retries:
        logger.warning("Max retries reached, returning best attempt")

    # --- Step 5: Store assistant response in memory ---
    if session_id:
        from memory.conversation import conversation_store

        conversation_store.add_message(session_id, "assistant", answer)

    score = parse_evaluation_score(evaluation)

    return {
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation,
        "score": score,
        "query_type": query_type,
        "plan": plan,
        "timing": timings,
    }
