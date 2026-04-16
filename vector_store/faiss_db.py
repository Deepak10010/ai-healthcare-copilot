import os
import logging

from langchain_community.vectorstores import FAISS

from config import settings

logger = logging.getLogger(__name__)


def create_vector_store(chunks, embeddings):
    """Create a new FAISS vector store from document chunks."""
    return FAISS.from_documents(chunks, embeddings)


def save_vector_store(db, path=None):
    """Persist FAISS index to disk."""
    path = path or settings.faiss_index_dir
    os.makedirs(path, exist_ok=True)
    db.save_local(path)
    logger.info(f"Vector store saved to {path}")


def load_vector_store(embeddings, path=None):
    """Load FAISS index from disk. Returns None if not found."""
    path = path or settings.faiss_index_dir
    index_file = os.path.join(path, "index.faiss")
    if os.path.exists(index_file):
        logger.info(f"Loading existing vector store from {path}")
        return FAISS.load_local(
            path, embeddings, allow_dangerous_deserialization=True
        )
    return None


def get_or_create_vector_store(chunks, embeddings, force_rebuild=False):
    """Load from disk if exists, otherwise build and save."""
    if not force_rebuild:
        db = load_vector_store(embeddings)
        if db is not None:
            logger.info("Using cached vector store from disk")
            return db

    logger.info("Building new vector store from documents")
    db = create_vector_store(chunks, embeddings)
    save_vector_store(db)
    return db


def add_documents_to_store(db, chunks, embeddings):
    """Incrementally add new documents to an existing FAISS store."""
    new_db = FAISS.from_documents(chunks, embeddings)
    db.merge_from(new_db)
    save_vector_store(db)
    logger.info(f"Added {len(chunks)} new chunks to vector store")
    return db
