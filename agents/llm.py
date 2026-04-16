from langchain_ollama import OllamaLLM

from config import settings

llm = OllamaLLM(
    model=settings.llm_model,
    base_url=settings.ollama_base_url,
)
