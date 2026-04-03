# Stores knowledge

from langchain_community.vectorstores import FAISS

def create_vector_store(chunks, embeddings):
    db = FAISS.from_documents(chunks, embeddings)
    return db