import os
import logging
import time

from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import settings
from logging_config import setup_logging
from ingestion.loader import load_all_documents, load_single_file, SUPPORTED_EXTENSIONS
from ingestion.chunking import split_documents
from ingestion.embedding import get_embeddings
from vector_store.faiss_db import get_or_create_vector_store, add_documents_to_store
from pipeline.rag_pipeline import ask_question_agentic
from memory.conversation import conversation_store

# --- Setup ---
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Healthcare Copilot API",
    description="Intelligent document-backed healthcare Q&A powered by RAG",
    version="2.0.0",
)

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"status": "error", "message": "Rate limit exceeded. Try again later."},
    )


# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if settings.api_key and api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# --- Global Error Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"},
    )


# --- Startup: Build Vector Store ---
logger.info("Initializing AI Healthcare Copilot API...")

docs = load_all_documents()
chunks = split_documents(docs)
logger.info(f"Total chunks: {len(chunks)}")

embeddings = get_embeddings()
db = get_or_create_vector_store(chunks, embeddings, force_rebuild=settings.force_rebuild)

logger.info("System ready!")


# --- Request/Response Models ---
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list = []
    evaluation: str | None = None
    score: int | None = None
    query_type: str | None = None
    timing: dict | None = None
    session_id: str | None = None
    status: str = "success"


# --- Endpoints ---
@app.get("/")
def home():
    return {"message": "AI Healthcare Copilot API is running", "version": "2.0.0"}


@app.get("/health")
def health():
    doc_count = 0
    try:
        doc_count = len(db.docstore._dict) if db else 0
    except Exception:
        pass

    return {
        "status": "healthy",
        "vector_store_loaded": db is not None,
        "documents_indexed": doc_count,
        "model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "rerank_enabled": settings.rerank_enabled,
        "router_enabled": settings.router_enabled,
    }


@app.post("/ask", response_model=AskResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def ask(request: Request, body: QueryRequest, _=Depends(verify_api_key)):
    start_time = time.time()

    # Auto-create session if provided ID doesn't exist
    session_id = body.session_id
    if session_id and not conversation_store.session_exists(session_id):
        session_id = conversation_store.create_session()

    result = ask_question_agentic(db, body.query, session_id=session_id)
    total_time = time.time() - start_time

    logger.info(f"Query processed in {total_time:.2f}s: {body.query[:50]}...")

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        evaluation=result.get("evaluation"),
        score=result.get("score"),
        query_type=result.get("query_type"),
        timing=result.get("timing"),
        session_id=session_id,
        status="success",
    )


@app.post("/session")
def create_session():
    session_id = conversation_store.create_session()
    return {"session_id": session_id}


@app.get("/session/{session_id}/history")
def get_history(session_id: str):
    if not conversation_store.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    history = conversation_store.get_history(session_id)
    return {
        "session_id": session_id,
        "messages": [{"role": m.role, "content": m.content} for m in history],
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...), _=Depends(verify_api_key)):
    global db

    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}",
        )

    # Validate file size (max 50MB)
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")

    # Save file securely
    safe_filename = os.path.basename(file.filename)
    save_path = os.path.join(settings.data_dir, safe_filename)
    with open(save_path, "wb") as f:
        f.write(content)

    logger.info(f"Uploaded file: {safe_filename}")

    # Ingest the new document
    try:
        new_docs = load_single_file(save_path)
        new_chunks = split_documents(new_docs)
        db = add_documents_to_store(db, new_chunks, embeddings)

        return {
            "status": "success",
            "message": f"Uploaded and indexed {safe_filename}",
            "pages_loaded": len(new_docs),
            "chunks_created": len(new_chunks),
        }
    except Exception as e:
        logger.error(f"Failed to ingest uploaded file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process uploaded file")
