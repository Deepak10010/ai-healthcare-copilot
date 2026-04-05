# AI Healthcare Copilot - Simple Architecture Diagram

```mermaid
architecture-beta
    group datasources(cloud)[Data Sources]
    group processing(cloud)[Processing Layer]
    group orchestration(cloud)[Orchestration]
    group aiservices(cloud)[AI Services]
    group retrieval(cloud)[Data Retrieval]
    group persistence(cloud)[Persistence]
    group monitoring(cloud)[Monitoring]

    service documents(disk)[Documents] in datasources
    service pdfloader(disk)[PDF Loader] in datasources

    service chunking(server)[Chunking] in processing
    service embedding(server)[Embedding] in processing
    service ingestion(server)[Ingestion] in processing

    service eventbus(server)[Event Bus] in orchestration
    service rag_orch(server)[RAG Orchestrator] in orchestration

    service planner_a(server)[Planner Agent] in aiservices
    service retriever_a(server)[Retriever Agent] in aiservices
    service generator_a(server)[Generator Agent] in aiservices
    service evaluator_a(server)[Evaluator Agent] in aiservices
    service llm(server)[LLM Service] in aiservices

    service query_h(server)[Query Handler] in retrieval
    service context_b(server)[Context Builder] in retrieval
    service response_f(server)[Response Formatter] in retrieval

    service vectordb(database)[Vector Store FAISS] in persistence
    service metadata(database)[Metadata Store] in persistence
    service cache(database)[Cache Layer] in persistence

    service apigateway(server)[API Gateway] in monitoring
    service monitoring_s(server)[Monitoring] in monitoring

    documents:R -- L:pdfloader
    pdfloader:R -- L:chunking
    chunking:R -- L:embedding
    embedding:R -- L:ingestion
    ingestion:R -- L:eventbus
    eventbus:R -- L:rag_orch

    rag_orch:B -- T:planner_a
    planner_a:R -- L:retriever_a
    retriever_a:R -- L:generator_a
    generator_a:R -- L:evaluator_a
    evaluator_a:B -- T:llm

    llm:B -- T:query_h
    query_h:R -- L:context_b
    context_b:R -- L:response_f

    response_f:B -- T:vectordb
    vectordb:L -- R:metadata
    metadata:L -- R:cache

    cache:B -- T:apigateway
    apigateway:R -- L:monitoring_s
```

## Overview

This diagram shows the clean, linear flow of the AI Healthcare Copilot architecture:

- **Left-to-Right Flow**: Data ingestion pipeline processing documents
- **Top-to-Bottom Flow**: Orchestration triggering AI agents and response formatting
- **Grouped Layers**: Seven distinct layers organizing components by function

Use this diagram for high-level architectural overview and presentations.
