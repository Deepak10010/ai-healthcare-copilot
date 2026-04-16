from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Paths
    data_dir: str = "data"
    faiss_index_dir: str = "vector_store/index"

    # Ingestion
    chunk_size: int = 500
    chunk_overlap: int = 50
    embedding_model: str = "all-MiniLM-L6-v2"

    # Retrieval
    retriever_k: int = 3
    context_max_chars: int = 2500
    rerank_enabled: bool = True
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    rerank_top_n: int = 3

    # LLM
    llm_model: str = "llama3"
    ollama_base_url: str = "http://host.docker.internal:11434"

    # API
    api_key: str = ""
    rate_limit_per_minute: int = 30
    cors_origins: list = ["*"]

    # Pipeline
    max_retries: int = 1
    router_enabled: bool = True

    # Logging
    log_level: str = "INFO"

    # Vector store
    force_rebuild: bool = False

    model_config = {"env_prefix": "COPILOT_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
