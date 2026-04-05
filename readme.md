graph LR
A[main.py] --> B[load_pdf]
B --> C[split_documents]
C --> D[get_embeddings]
D --> E[create_vector_store]
E --> F[ask_question]
F --> G[Ollama LLM]

🔁 Step-by-step flow:

1. main.py

👉 Starts everything

2. loader.py

👉 Reads PDF → extracts text

3. chunking.py

👉 Splits text into chunks

4. embedding.py

👉 Converts chunks → vectors

5. faiss_db.py

👉 Stores vectors in database

6. User query comes in
7. rag_pipeline.py
   🔎 Retrieve:

Finds relevant chunks

🧠 Build context:

Combines them

🤖 Generate:

LLM answers using context

8. main.py

👉 Prints final answer

🎯 ONE-LINE SUMMARY FOR EACH FILE
File Role
main.py Orchestrates everything
loader.py Loads raw data
chunking.py Splits data
embedding.py Converts text → vectors
faiss_db.py Stores & searches vectors
rag_pipeline.py Retrieves + generates answer
🧠 SIMPLE ANALOGY (SUPER IMPORTANT)

Imagine building a smart librarian system 📚

Component Real World
loader Reads books
chunking Breaks books into paragraphs
embeddings Converts meaning into numbers
vector DB Stores knowledge
retriever Finds relevant info
LLM Explains answer
main.py Controls the process

# To activate the virtual environment

.\venv\Scripts\Activate.ps1

flowchart TD
A[main.py] --> B[build_vector_db]
B --> C[load_pdf<br/>from ingestion/loader.py]
C --> D[split_documents<br/>from ingestion/chunking.py]
D --> E[get_embeddings<br/>from ingestion/embedding.py]
E --> F[create_vector_store<br/>from vector_store/faiss_db.py]
F --> G[Vector DB Ready]

    G --> H[run_query_loop]
    H --> I[User Input Query]
    I --> J[ask_question_agentic<br/>from pipeline/rag_pipeline.py]

    J --> K[Planner Agent<br/>agents/planner.py<br/>Breaks query into steps]
    K --> L[Retriever Agent<br/>agents/retriever.py<br/>Fetches relevant context]
    L --> M[Generator Agent<br/>agents/generator.py<br/>Produces final answer]
    M --> N[Display Answer]
    N --> O{Continue?}
    O -->|Yes| I
    O -->|No| P[Exit]

# To launch the backend

uvicorn api.app:app --reload

# To launch the frontend

streamlit run ui/app.py


# To build Docker image
docker build -t ai-copilot .

# To run container
docker run -p 8000:8000 ai-copilot

# To build Docker image
docker compose build --no-cache

# To run the Docker image
docker compose up