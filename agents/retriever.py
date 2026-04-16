import logging

from config import settings

logger = logging.getLogger(__name__)


def retriever_agent(db, query: str, strategy: dict = None) -> dict:
    """Retrieve relevant documents and return context with source citations.

    Returns:
        dict with keys: context (str), sources (list[dict]), raw_docs (list)
    """
    k = settings.retriever_k
    context_limit = settings.context_max_chars

    if strategy:
        k = int(k * strategy.get("k_multiplier", 1))
        context_limit = strategy.get("context_limit", context_limit)

    # Over-fetch if re-ranking is enabled (re-ranker will trim)
    fetch_k = k * 2 if settings.rerank_enabled else k

    retriever = db.as_retriever(search_kwargs={"k": fetch_k})
    docs = retriever.invoke(query)
    logger.info(f"Retrieved {len(docs)} raw documents (k={fetch_k})")

    # Re-rank if enabled
    if settings.rerank_enabled and docs:
        try:
            from agents.reranker import rerank_documents

            docs = rerank_documents(query, docs, top_n=k)
            logger.info(f"Re-ranked to top {len(docs)} documents")
        except Exception as e:
            logger.warning(f"Re-ranking failed, using raw results: {e}")
            docs = docs[:k]
    else:
        docs = docs[:k]

    # Build context string
    context = "\n\n".join(doc.page_content for doc in docs)
    context = context[:context_limit]

    # Extract source citations (deduplicated)
    sources = []
    seen = set()
    for doc in docs:
        source_key = (
            doc.metadata.get("source", "Unknown"),
            doc.metadata.get("page", None),
        )
        if source_key not in seen:
            seen.add(source_key)
            sources.append(
                {"document": source_key[0], "page": source_key[1]}
            )

    logger.info(f"Context: {len(context)} chars from {len(sources)} sources")

    return {
        "context": context,
        "sources": sources,
        "raw_docs": docs,
    }
