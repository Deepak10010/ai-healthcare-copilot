import os
from ingestion.loader import load_pdf
from ingestion.chunking import split_documents
from ingestion.embedding import get_embeddings
from vector_store.faiss_db import create_vector_store
from pipeline.rag_pipeline import ask_question
from dotenv import load_dotenv

load_dotenv()

# Step 1: Load
docs = load_pdf("data/sample.pdf")

# Step 2: Chunk
chunks = split_documents(docs)

# Step 3: Embeddings
embeddings = get_embeddings()

# Step 4: Vector DB
db = create_vector_store(chunks, embeddings)

# Step 5: Ask Question
query = "What is hypertension?"
answer = ask_question(db, query)

print("\nANSWER:\n", answer)