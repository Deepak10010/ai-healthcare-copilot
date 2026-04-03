from fastapi import FastAPI
from pydantic import BaseModel

from ingestion.loader import load_all_pdfs
from ingestion.chunking import split_documents
from ingestion.embedding import get_embeddings
from vector_store.faiss_db import create_vector_store
from pipeline.rag_pipeline import ask_question_agentic

app = FastAPI()


# -------- Load ALL documents at startup --------
print("📥 Loading all PDFs from data folder...")
docs = load_all_pdfs("data")

print(f"📄 Total documents loaded: {len(docs)}")

print("✂️ Splitting into chunks...")
chunks = split_documents(docs)

print(f"📊 Total chunks: {len(chunks)}")

print("🔢 Generating embeddings...")
embeddings = get_embeddings()

print("🗄️ Creating vector DB...")
db = create_vector_store(chunks, embeddings)

print("✅ System ready!")


# -------- Request Schema --------
class QueryRequest(BaseModel):
    query: str


# -------- Health Check --------
@app.get("/")
def home():
    return {"message": "AI Healthcare Copilot API is running 🚀"}


# -------- Main Endpoint --------
@app.post("/ask")
def ask(request: QueryRequest):
    try:
        result = ask_question_agentic(db, request.query)
        return {
            "answer": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "answer": "Something went wrong",
            "error": str(e),
            "status": "error"
        }