# 🏥 AI Healthcare Copilot

An intelligent document-backed question-answering system powered by Retrieval-Augmented Generation (RAG) and multi-agent AI orchestration. This framework enables healthcare professionals to query medical documents, PDFs, and knowledge bases using natural language.

## 🌟 Features

- **🤖 Multi-Agent Architecture** - Specialized agents for planning, retrieval, generation, and evaluation
- **📚 RAG Pipeline** - Retrieves relevant context from documents and generates accurate, context-aware responses
- **⚡ FAISS Vector Store** - Fast similarity search across document embeddings
- **🧠 LLM Integration** - Seamless integration with language models (Ollama-compatible)
- **🎯 Intelligent Query Planning** - Breaks down complex queries into actionable steps
- **📄 Multi-Format Support** - Loads and processes PDFs and other documents
- **🐳 Containerized** - Full Docker and Docker Compose support for easy deployment
- **🌐 Web UI** - Streamlit-based frontend for user interactions
- **⚙️ REST API** - FastAPI backend for programmatic access

## 🏗️ Architecture Overview

The system follows a layered architecture with five main components:

```
User Interface (Streamlit)
         ↓
   API Server (FastAPI)
         ↓
   RAG Pipeline Service
         ↓
   Multi-Agent System
   ├─ LLM Service
   ├─ Planner Agent
   ├─ Generator Agent
   ├─ Evaluator Agent
   └─ Retriever Agent
         ↓
   Vector Store (FAISS)
```

**Data Flow:**

1. Documents are loaded and split into chunks
2. Chunks are converted to embeddings
3. Embeddings are stored in FAISS vector database
4. User queries trigger the multi-agent pipeline
5. Relevant context is retrieved and used to generate responses

## 📋 Prerequisites

Before getting started, ensure you have the following installed on your system:

### **Required Software**

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Docker** (optional, for containerized deployment) - [Download](https://www.docker.com/products/docker-desktop)
- **Git** - [Download](https://git-scm.com/downloads)

### **System Requirements**

- **RAM**: Minimum 4GB (8GB+ recommended for LLM operations)
- **Disk Space**: 5GB+ for models and vector databases
- **Internet**: Required for downloading dependencies and models

## 🚀 Installation & Setup

### **Option 1: Local Setup (Recommended for Development)**

#### **Windows**

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-healthcare-copilot.git
   cd ai-healthcare-copilot
   ```

2. **Create a Python virtual environment**

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install backend dependencies**

   ```bash
   pip install -r requirements-backend.txt
   ```

4. **Install frontend dependencies**

   ```bash
   pip install -r requirements-frontend.txt
   ```

5. **Verify Installation**
   ```bash
   python -c "import torch, langchain, faiss; print('All dependencies installed successfully!')"
   ```

#### **macOS / Linux**

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-healthcare-copilot.git
   cd ai-healthcare-copilot
   ```

2. **Create a Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install backend dependencies**

   ```bash
   pip install -r requirements-backend.txt
   ```

4. **Install frontend dependencies**
   ```bash
   pip install -r requirements-frontend.txt
   ```

### **Option 2: Docker Deployment (Recommended for Production)**

1. **Build the Docker image**

   ```bash
   docker compose build --no-cache
   ```

2. **Run the containerized application**

   ```bash
   docker compose up
   ```

   The application will be available at:
   - Frontend: `http://localhost:8501`
   - Backend API: `http://localhost:8000`

## 🎯 How to Run

### **Local Development**

#### **Start the Backend API Server**

```bash
# Windows
.\venv\Scripts\Activate.ps1
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

# macOS / Linux
source venv/bin/activate
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://localhost:8000`

#### **Start the Frontend (in a new terminal)**

```bash
# Windows
.\venv\Scripts\Activate.ps1
streamlit run ui/app.py

# macOS / Linux
source venv/bin/activate
streamlit run ui/app.py
```

The UI will open at `http://localhost:8501`

#### **Run the Main Script**

```bash
# Windows
.\venv\Scripts\Activate.ps1
python main.py

# macOS / Linux
source venv/bin/activate
python main.py
```

### **Docker Deployment**

```bash
# Build and run all services
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## 📁 Project Structure

```
ai-healthcare-copilot/
├── main.py                    # Entry point for CLI application
├── requirements-backend.txt   # Backend Python dependencies
├── requirements-frontend.txt  # Frontend Python dependencies
├── docker-compose.yml         # Docker compose configuration
├── Dockerfile.backend         # Backend container definition
├── Dockerfile.frontend        # Frontend container definition
│
├── agents/                    # AI Agent modules
│   ├── planner.py            # Query planning agent
│   ├── retriever.py          # Document retrieval agent
│   ├── generator.py          # Response generation agent
│   ├── evaluator.py          # Response evaluation agent
│   └── llm.py                # LLM service wrapper
│
├── api/                       # FastAPI backend
│   └── app.py                # REST API endpoints
│
├── ingestion/                 # Data processing pipeline
│   ├── loader.py             # Document loading
│   ├── chunking.py           # Text chunking strategies
│   └── embedding.py          # Embedding generation
│
├── pipeline/                  # Core processing pipeline
│   └── rag_pipeline.py       # RAG orchestration
│
├── vector_store/              # Vector database
│   └── faiss_db.py           # FAISS vector store management
│
├── ui/                        # Streamlit frontend
│   └── app.py                # Web interface
│
└── data/                      # Data storage
    ├── pdfs/                 # Input PDF documents
    └── vector_db/            # Persisted vector store
```

## 🔄 Workflow: From Documents to Answers

### **1. Data Ingestion Phase**

```
PDF Document → loader.py → Extract Text
         ↓
    chunking.py → Split into Chunks
         ↓
    embedding.py → Generate Embeddings
         ↓
    faiss_db.py → Store in Vector DB
```

### **2. Query Processing Phase**

```
User Query
   ↓
Planner Agent → Break Query into Steps
   ↓
Retriever Agent → Fetch Relevant Context
   ↓
Generator Agent → Generate Response
   ↓
Evaluator Agent → Assess Quality
   ↓
Display Answer
```

## 🛠️ API Endpoints

### **Health Check**

```bash
curl http://localhost:8000/health
```

### **Query Endpoint**

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the symptoms of diabetes?",
    "top_k": 5
  }'
```

### **Ingest Document**

```bash
curl -X POST http://localhost:8000/api/ingest \
  -F "file=@path/to/document.pdf"
```

## 📦 Adding Custom Documents

1. **Place your PDF files** in the `data/pdfs/` directory
2. **Run the ingestion pipeline**:
   ```bash
   python main.py --ingest
   ```
3. **Query your documents** via the UI or API

## 🐛 Troubleshooting

### **Virtual Environment Issues (Windows)**

```bash
# If activation fails, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### **Port Already in Use**

```bash
# Change the port in your startup command:
uvicorn api.app:app --reload --port 8001
streamlit run ui/app.py --server.port 8502
```

### **FAISS Build Errors**

```bash
# Reinstall FAISS from conda
conda install -c conda-forge faiss-cpu
```

### **Out of Memory**

- Reduce the chunk size in `ingestion/chunking.py`
- Use a smaller embedding model
- Process documents in batches

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request



## 👤 Author

**Deepak Lokanath**

---

**Happy Querying! 🚀**
