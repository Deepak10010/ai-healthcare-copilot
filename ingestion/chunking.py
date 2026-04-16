from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(documents)
