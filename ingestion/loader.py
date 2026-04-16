import os
import logging

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

from config import settings

logger = logging.getLogger(__name__)

LOADER_REGISTRY = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".docx": Docx2txtLoader,
}

SUPPORTED_EXTENSIONS = set(LOADER_REGISTRY.keys())


def load_single_file(file_path: str):
    """Load a single document file using the appropriate loader."""
    ext = os.path.splitext(file_path)[1].lower()
    loader_cls = LOADER_REGISTRY.get(ext)
    if loader_cls is None:
        logger.warning(f"Unsupported file type: {ext} ({file_path})")
        return []
    loader = loader_cls(file_path)
    docs = loader.load()
    filename = os.path.basename(file_path)
    for doc in docs:
        doc.metadata["source"] = filename
    return docs


def load_all_documents(folder_path: str = None):
    """Load all supported documents (PDF, TXT, DOCX) from a folder."""
    folder_path = folder_path or settings.data_dir
    documents = []

    if not os.path.exists(folder_path):
        logger.error(f"Data directory not found: {folder_path}")
        return documents

    for file in os.listdir(folder_path):
        ext = os.path.splitext(file)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            file_path = os.path.join(folder_path, file)
            try:
                docs = load_single_file(file_path)
                documents.extend(docs)
                logger.info(f"Loaded {len(docs)} pages from {file}")
            except Exception as e:
                logger.error(f"Failed to load {file}: {e}")

    logger.info(f"Total documents loaded: {len(documents)}")
    return documents


# Backward compatibility alias
def load_all_pdfs(folder_path: str):
    return load_all_documents(folder_path)
