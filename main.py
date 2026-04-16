import logging

from config import settings
from logging_config import setup_logging
from ingestion.loader import load_all_documents
from ingestion.chunking import split_documents
from ingestion.embedding import get_embeddings
from vector_store.faiss_db import get_or_create_vector_store
from pipeline.rag_pipeline import ask_question_agentic

setup_logging()
logger = logging.getLogger(__name__)


def build_vector_db():
    logger.info("Loading documents...")
    docs = load_all_documents()
    logger.info(f"Total documents loaded: {len(docs)}")

    logger.info("Splitting into chunks...")
    chunks = split_documents(docs)
    logger.info(f"Total chunks created: {len(chunks)}")

    logger.info("Generating embeddings...")
    embeddings = get_embeddings()

    logger.info("Building vector database...")
    db = get_or_create_vector_store(
        chunks, embeddings, force_rebuild=settings.force_rebuild
    )
    logger.info("Vector DB ready!")
    return db


def run_query_loop(db):
    print("\nYou can now ask questions (type 'exit' to quit)\n")

    while True:
        query = input("Enter your question: ")

        if query.lower() == "exit":
            print("\nExiting... Goodbye!")
            break

        result = ask_question_agentic(db, query)

        print(f"\nAnswer:\n{result['answer']}")

        if result.get("sources"):
            print("\nSources:")
            for src in result["sources"]:
                page = src.get("page")
                page_text = f", Page {page + 1}" if page is not None else ""
                print(f"  - {src['document']}{page_text}")

        print(f"\nQuery type: {result.get('query_type', 'N/A')}")
        print(f"Confidence: {result.get('score', 'N/A')}/10")
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    db = build_vector_db()
    run_query_loop(db)
