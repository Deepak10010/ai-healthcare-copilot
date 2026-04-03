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
File	Role
main.py	Orchestrates everything
loader.py	Loads raw data
chunking.py	Splits data
embedding.py	Converts text → vectors
faiss_db.py	Stores & searches vectors
rag_pipeline.py	Retrieves + generates answer
🧠 SIMPLE ANALOGY (SUPER IMPORTANT)

Imagine building a smart librarian system 📚

Component	Real World
loader	Reads books
chunking	Breaks books into paragraphs
embeddings	Converts meaning into numbers
vector DB	Stores knowledge
retriever	Finds relevant info
LLM	Explains answer
main.py	Controls the process



# To activate the virtual environment
.\venv\Scripts\Activate.ps1  

