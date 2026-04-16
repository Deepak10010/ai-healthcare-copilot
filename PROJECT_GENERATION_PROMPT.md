# Project Generation Prompt

Use the following prompt with an AI coding assistant (e.g., Claude Code) to generate a complete RAG-based multi-agent healthcare copilot project from scratch.

---

## The Prompt

```
Build a complete AI Healthcare Copilot application — an intelligent, document-backed
question-answering system powered by Retrieval-Augmented Generation (RAG) and multi-agent
AI orchestration. Healthcare professionals should be able to query medical documents (PDFs)
using natural language and receive accurate, context-grounded answers.

The system must have three access interfaces: a CLI, a REST API (FastAPI), and a web UI
(Streamlit). It must be fully containerized with Docker Compose.

---

## Architecture

Use a layered architecture with these five layers:

1. **User Interface Layer** — Streamlit web app + CLI REPL
2. **API Layer** — FastAPI REST backend
3. **Orchestration Layer** — RAG pipeline that coordinates multi-agent execution
4. **Agent Layer** — Four specialized agents (Planner, Retriever, Generator, Evaluator)
5. **Data Layer** — FAISS vector store + PDF document ingestion pipeline

Data flows top-down: UI/CLI -> API -> Pipeline -> Agents -> Vector Store.

---

## Project Structure

Create this exact directory layout (no __init__.py files — use implicit namespace packages):

```
project-root/
├── main.py                        # CLI entry point
├── requirements-backend.txt       # Backend Python dependencies
├── requirements-frontend.txt      # Frontend Python dependencies
├── docker-compose.yml             # Container orchestration
├── Dockerfile.backend             # Backend container
├── Dockerfile.frontend            # Frontend container
├── agents/                        # AI agent modules
│   ├── llm.py                     # LLM service wrapper (singleton)
│   ├── planner.py                 # Query planning agent
│   ├── retriever.py               # Document retrieval agent
│   ├── generator.py               # Response generation agent
│   └── evaluator.py               # Response quality evaluation agent
├── api/                           # REST API
│   └── app.py                     # FastAPI application
├── ingestion/                     # Data processing pipeline
│   ├── loader.py                  # PDF document loading
│   ├── chunking.py                # Text chunking
│   └── embedding.py               # Embedding generation
├── pipeline/                      # Core orchestration
│   └── rag_pipeline.py            # Multi-agent RAG orchestrator
├── vector_store/                  # Vector database
│   └── faiss_db.py                # FAISS vector store management
├── ui/                            # Web frontend
│   └── app.py                     # Streamlit application
└── data/                          # Data storage (for PDFs)
```

---

## Component Specifications

### 1. LLM Service (`agents/llm.py`)

- Create a single global LLM instance using LangChain's `ChatAnthropic` from `langchain_anthropic`.
- Model: "claude-sonnet-4-20250514"
- The API key is read from the `ANTHROPIC_API_KEY` environment variable (ChatAnthropic does
  this automatically).
- This is the shared LLM used by all agents.
- Since ChatAnthropic is a chat model, agent functions should use `llm.invoke(prompt)` which
  accepts a string and returns an AIMessage. Extract the text with `.content`.

### 2. Planner Agent (`agents/planner.py`)

- Pure function: `planner_agent(query: str) -> str`
- Prompt the LLM to act as a "planning agent for a RAG system."
- Instructions in the prompt must include:
  - ONLY break down the user query into simple retrieval-focused steps
  - DO NOT add external knowledge
  - DO NOT assume facts not in the query
  - Keep it short and relevant
- Call `llm.invoke(prompt)` and return `.content` (the text string from the AIMessage).

### 3. Retriever Agent (`agents/retriever.py`)

- Pure function: `retriever_agent(db, query: str) -> str`
- Convert the FAISS vector store to a LangChain retriever with `search_kwargs={"k": 3}`.
- Invoke the retriever with the query.
- Concatenate the `page_content` of all returned documents with "\n\n" separators.
- Truncate the result to 2500 characters maximum.

### 4. Generator Agent (`agents/generator.py`)

- Pure function: `generator_agent(query: str, context: str) -> str`
- Prompt the LLM to act as a "medical assistant."
- Instructions must include:
  - Use ONLY the provided context to answer the question
  - If the answer is not in the context, say exactly: "I don't know based on the provided documents."
- Inject the context and query into the prompt via f-string template.
- Call `llm.invoke(prompt)` and return `.content`.

### 5. Evaluator Agent (`agents/evaluator.py`)

- Pure function: `evaluator_agent(query: str, context: str, answer: str) -> str`
- Prompt the LLM to act as an "AI evaluator."
- Evaluation criteria:
  1. Is the answer supported by the context?
  2. Is it relevant to the question?
  3. Is there any hallucination?
- Require output in this exact format:
  - Score: (0-10)
  - Verdict: (GOOD / BAD)
  - Feedback: (short explanation)
- Call `llm.invoke(prompt)` and return `.content`.

### 6. RAG Pipeline (`pipeline/rag_pipeline.py`)

- Function: `ask_question_agentic(db, query: str, max_retries: int = 0) -> str`
- Orchestration flow:
  1. Call `planner_agent(query)` and print the plan
  2. Call `retriever_agent(db, query)` and print first 1000 chars of context
  3. Enter a retry loop (up to `max_retries`):
     a. Call `generator_agent(query, context)` to produce an answer
     b. Call `evaluator_agent(query, context, answer)` to evaluate it
     c. If the evaluation contains "GOOD" (case-insensitive), accept and return the answer
     d. Otherwise, print a retry message and loop
  4. If max retries exhausted, return the last generated answer with a warning print.
- Print intermediate steps to console for debugging transparency.

### 7. Document Loader (`ingestion/loader.py`)

- Function: `load_all_pdfs(folder_path: str) -> list`
- Scan the folder for files ending in ".pdf" (case-insensitive).
- Use LangChain's `PyPDFLoader` to load each PDF.
- Enrich each document's metadata with `{"source": filename}`.
- Return the accumulated list of LangChain Document objects.

### 8. Text Chunker (`ingestion/chunking.py`)

- Function: `split_documents(documents) -> list`
- Use LangChain's `RecursiveCharacterTextSplitter` with:
  - `chunk_size=500`
  - `chunk_overlap=50`
- Return the list of chunked Document objects.

### 9. Embedding Generator (`ingestion/embedding.py`)

- Function: `get_embeddings()` that returns a `HuggingFaceEmbeddings` instance.
- Model: "all-MiniLM-L6-v2" (384 dimensions, lightweight, CPU-friendly).

### 10. Vector Store (`vector_store/faiss_db.py`)

- Function: `create_vector_store(chunks, embeddings)` that returns a FAISS vector store.
- Use LangChain's `FAISS.from_documents(chunks, embeddings)`.

### 11. CLI Entry Point (`main.py`)

- `build_vector_db()` function:
  - Call `load_all_pdfs("data")` to load documents
  - Call `split_documents()` to chunk them
  - Call `get_embeddings()` to get the embedding model
  - Call `create_vector_store()` to build the FAISS index
  - Return the vector store
- `run_query_loop(db)` function:
  - Infinite loop prompting user for input
  - Exit on "exit" command
  - Call `ask_question_agentic(db, query)` for each query
  - Print the answer
- `if __name__ == "__main__"`: build the DB then start the query loop.

### 12. FastAPI Backend (`api/app.py`)

- On module load (startup), eagerly run the full ingestion pipeline:
  load PDFs -> chunk -> embed -> create vector store. Store the DB globally.
- Define a Pydantic model: `QueryRequest` with a `query: str` field.
- Endpoints:
  - `GET /` — Returns `{"message": "AI Healthcare Copilot API is running"}` (health check)
  - `POST /ask` — Accepts `QueryRequest`, calls `ask_question_agentic(db, request.query)`,
    returns `{"answer": result, "status": "success"}`.
    On exception, catch it with traceback and return
    `{"answer": "Something went wrong", "error": str(e), "traceback": traceback.format_exc(), "status": "error"}`.

### 13. Streamlit Frontend (`ui/app.py`)

- Page config: title "AI Healthcare Copilot", icon "🩺", centered layout.
- Components:
  - Title header
  - Text input: "Ask a healthcare question:"
  - Submit button
- On submit:
  - POST to `http://backend:8000/ask` with `{"query": query}`, timeout 180s.
  - Display raw JSON response with `st.json()`.
  - If status is "success", display the answer with `st.write()`.
  - If status is "error", show error message and traceback in an expander.
  - Catch request exceptions and display with `st.error()`.

---

## Docker Configuration

### docker-compose.yml

Two services:

**backend:**
- Build from Dockerfile.backend (context: project root)
- Container name: ai-copilot-backend
- Port mapping: 8000:8000
- Pass the ANTHROPIC_API_KEY environment variable from host: `environment: - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}`
- Restart policy: unless-stopped

**frontend:**
- Build from Dockerfile.frontend (context: project root)
- Container name: ai-copilot-frontend
- Port mapping: 8501:8501
- Depends on: backend
- Restart policy: unless-stopped

### Dockerfile.backend

- Base: python:3.10-slim
- Install build-essential and curl via apt-get (clean up apt cache after)
- Set PYTHONUNBUFFERED=1
- Copy and install requirements-backend.txt
- Copy project files
- Expose 8000
- CMD: uvicorn api.app:app --host 0.0.0.0 --port 8000

### Dockerfile.frontend

- Base: python:3.10-slim
- Set PYTHONUNBUFFERED=1
- Copy and install requirements-frontend.txt
- Copy project files
- Expose 8501
- CMD: streamlit run ui/app.py --server.port=8501 --server.address=0.0.0.0

---

## Dependencies

### requirements-backend.txt

```
fastapi
uvicorn
requests
langchain
langchain-community
langchain-core
langchain-text-splitters
langchain-anthropic
langchain-huggingface
sentence-transformers
faiss-cpu
pypdf
```

### requirements-frontend.txt

```
streamlit
requests
```

---

## Key Design Principles

1. **Agents as pure functions** — No state, no classes. Each agent is a single function
   that takes inputs and returns a string. The LLM is a shared singleton.

2. **Prompt engineering with guardrails** — Use negative prompting ("DO NOT add external
   knowledge") and explicit fallback instructions ("say I don't know") to prevent
   hallucination.

3. **Evaluation-gated generation** — The Evaluator agent acts as a quality gate. Answers
   must pass evaluation before being returned. Failed answers trigger regeneration.

4. **Context truncation** — Retrieved context is hard-capped at 2500 characters to keep
   responses focused and cost-efficient, even though Claude supports much larger contexts.

5. **Eager initialization** — The API server loads and indexes all documents at startup
   so queries are fast at runtime.

6. **Console transparency** — Print all intermediate agent outputs (plans, context,
   evaluations) to console for debugging.

7. **Minimal abstractions** — No unnecessary wrappers, base classes, or design patterns.
   Each file is short and does one thing.

---

## Prerequisites

- An Anthropic API key. Set it as an environment variable: `export ANTHROPIC_API_KEY=your-key-here`
- Place PDF documents in the `data/` folder before running.
- Python 3.10+ for local development.
- Docker and Docker Compose for containerized deployment.
```

---

## Usage Notes

- Copy everything inside the code fence above and paste it as a prompt to an AI coding assistant.
- The prompt is self-contained and should produce a fully functional project.
- Set your `ANTHROPIC_API_KEY` environment variable before running.
- Place your medical PDF documents in the `data/` folder.
- To adapt for a different domain (e.g., legal, finance), change the agent prompts from "medical assistant" to the appropriate role and adjust the document corpus.
