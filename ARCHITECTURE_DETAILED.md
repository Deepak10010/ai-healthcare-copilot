# AI Healthcare Copilot - Detailed Multi-Directional Architecture Diagram

```mermaid
graph TB
    subgraph DataSources["📥 DATA SOURCES"]
        Documents["📄 Medical Documents"]:::dataSource
        PDFLoader["📥 PDF Loader"]:::dataSource
    end

    subgraph Processing["⚙️ PROCESSING LAYER"]
        Chunking["📋 Document Chunking"]:::processing
        Embedding["🔢 Embedding Generation"]:::processing
        Ingestion["🔄 Ingestion Pipeline"]:::processing
    end

    subgraph Orchestration["🔄 ORCHESTRATION"]
        EventBus["📡 Event Bus"]:::orchestration
        RAGOrch["🎯 RAG Orchestrator"]:::orchestration
    end

    subgraph AIAgents["🧠 AI SERVICES LAYER"]
        Planner["📊 Planner Agent"]:::aiagent
        Retriever["🔍 Retriever Agent"]:::aiagent
        Generator["✍️ Generator Agent"]:::aiagent
        Evaluator["✅ Evaluator Agent"]:::aiagent
        LLM["🤖 LLM Service"]:::aiagent
    end

    subgraph Retrieval["🔍 DATA RETRIEVAL"]
        QueryHandler["❓ Query Handler"]:::retrieval
        ContextBuilder["📚 Context Builder"]:::retrieval
        ResponseFormatter["📝 Response Formatter"]:::retrieval
    end

    subgraph Persistence["💾 PERSISTENCE & STORAGE"]
        VectorDB["🗃️ Vector Store FAISS"]:::persistence
        MetadataStore["🏷️ Metadata Store"]:::persistence
        CacheLayer["⚡ Cache Layer"]:::persistence
    end

    subgraph Monitoring["📊 MONITORING & ACCESS"]
        APIGateway["🌐 API Gateway"]:::monitoring
        MonitoringService["📈 Monitoring Service"]:::monitoring
    end

    Documents -->|Ingest| PDFLoader
    PDFLoader -->|Process| Chunking
    Chunking -->|Transform| Embedding
    Embedding -->|Load| Ingestion
    Ingestion -->|Emit| EventBus
    EventBus -->|Trigger| RAGOrch

    RAGOrch -->|Plan| Planner
    Planner -->|Route| Retriever
    Retriever -->|Coordinate| Generator
    Generator -->|Review| Evaluator
    Evaluator -->|Generate| LLM

    LLM -->|Query| QueryHandler
    QueryHandler -->|Build| ContextBuilder
    ContextBuilder -->|Format| ResponseFormatter

    ResponseFormatter -->|Store| VectorDB
    ResponseFormatter -->|Write| MetadataStore
    ResponseFormatter -->|Cache| CacheLayer

    VectorDB -->|Retrieve| Retriever
    MetadataStore -->|Retrieve| ContextBuilder
    CacheLayer -->|Retrieve| QueryHandler

    RAGOrch -.->|Input| Monitoring
    Monitoring -->|Expose| APIGateway
    APIGateway -->|Monitor| MonitoringService

    MonitoringService -.->|Feedback| RAGOrch

    classDef dataSource fill:#FF6B6B,stroke:#C92A2A,stroke-width:2px,color:#fff
    classDef processing fill:#4ECDC4,stroke:#0BA5A5,stroke-width:2px,color:#fff
    classDef orchestration fill:#FFE66D,stroke:#D4A500,stroke-width:2px,color:#000
    classDef aiagent fill:#95E1D3,stroke:#38A169,stroke-width:2px,color:#000
    classDef retrieval fill:#A8D5FF,stroke:#0084FF,stroke-width:2px,color:#fff
    classDef persistence fill:#C9A2E0,stroke:#7C3AED,stroke-width:2px,color:#fff
    classDef monitoring fill:#FFB366,stroke:#FF8C00,stroke-width:2px,color:#fff
```

## Overview

This detailed diagram shows the complete multi-directional flow of the AI Healthcare Copilot architecture:

### **Vertical Flows (Top-to-Bottom)**

- Data ingestion pipeline flowing downward through processing layers
- Orchestration triggering AI agents
- Response formatting and storage

### **Horizontal Flows (Left-to-Right & Right-to-Left)**

- Retriever Agent pulling from Vector Store
- Context Builder pulling from Metadata Store
- Query Handler pulling from Cache Layer
- Data retrieval flows happening in parallel

### **Feedback Loops (Dotted Lines)**

- Monitoring data flowing back to RAG Orchestrator for continuous optimization
- Real-time feedback mechanisms for system improvement

### **Color-Coded Layers**

- 🔴 **Red**: Data Sources
- 🔵 **Teal**: Processing Layer
- 🟡 **Yellow**: Orchestration
- 🟢 **Green**: AI Services
- 🔵 **Light Blue**: Data Retrieval
- 🟣 **Purple**: Persistence & Storage
- 🟠 **Orange**: Monitoring & Access

Use this diagram for detailed technical documentation and internal presentations.
