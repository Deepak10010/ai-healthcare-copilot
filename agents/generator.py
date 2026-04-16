import logging

from agents.llm import llm

logger = logging.getLogger(__name__)


def generator_agent(query: str, context: str, chat_history: str = "") -> str:
    """Generate an answer using the LLM grounded in retrieved context.

    Args:
        query: The user's question
        context: Retrieved document text to base the answer on
        chat_history: Optional conversation history for follow-up questions
    """
    history_block = ""
    if chat_history:
        history_block = f"""
Previous Conversation:
{chat_history}

Use the conversation history above to understand follow-up questions.
"""

    prompt = f"""You are a medical assistant.
{history_block}
Use ONLY the provided context to answer the question.
If the answer is not in the context, say exactly:
"I don't know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
    logger.info(f"Generating answer (context: {len(context)} chars, history: {len(chat_history)} chars)")
    return llm.invoke(prompt)
