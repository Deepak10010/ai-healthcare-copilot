import os
from ingestion.loader import load_all_pdfs
from ingestion.chunking import split_documents
from ingestion.embedding import get_embeddings
from vector_store.faiss_db import create_vector_store
from pipeline.rag_pipeline import ask_question_agentic


def build_vector_db():
    print("\n📥 Loading documents...")
    docs = load_all_pdfs("data")  # ✅ MULTI-PDF

    print(f"\n📄 Total documents loaded: {len(docs)}")

    print("\n✂️ Splitting into chunks...")
    chunks = split_documents(docs)

    print(f"\n📊 Total chunks created: {len(chunks)}")

    print("\n🔢 Generating embeddings...")
    embeddings = get_embeddings()

    print("\n🗄️ Creating vector database...")
    db = create_vector_store(chunks, embeddings)

    print("\n✅ Vector DB ready!\n")

    return db


def run_query_loop(db):
    print("\n💬 You can now ask questions (type 'exit' to quit)\n")

    while True:
        query = input("👉 Enter your question: ")

        if query.lower() == "exit":
            print("\n👋 Exiting... Goodbye!")
            break

        answer = ask_question_agentic(db, query)

        print("\n💡 Answer:\n")
        print(answer)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    db = build_vector_db()
    run_query_loop(db)