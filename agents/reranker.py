import logging

from sentence_transformers import CrossEncoder

from config import settings

logger = logging.getLogger(__name__)

_model = None


def get_reranker():
    """Lazy-load the cross-encoder model."""
    global _model
    if _model is None:
        logger.info(f"Loading re-ranker model: {settings.rerank_model}")
        _model = CrossEncoder(settings.rerank_model)
    return _model


def rerank_documents(query: str, docs: list, top_n: int = None) -> list:
    """Re-rank retrieved docs using cross-encoder for better precision.

    Args:
        query: The user's search query
        docs: List of LangChain Document objects from FAISS retrieval
        top_n: Number of top documents to return after re-ranking

    Returns:
        List of top_n documents sorted by cross-encoder relevance score
    """
    top_n = top_n or settings.rerank_top_n

    if not docs:
        return docs

    model = get_reranker()
    pairs = [(query, doc.page_content) for doc in docs]
    scores = model.predict(pairs)

    scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    results = [doc for doc, score in scored_docs[:top_n]]

    logger.info(
        f"Re-ranked {len(docs)} docs -> top {len(results)} "
        f"(scores: {[f'{s:.3f}' for _, s in scored_docs[:top_n]]})"
    )
    return results
