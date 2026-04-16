from langchain_huggingface import HuggingFaceEmbeddings

from config import settings


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
