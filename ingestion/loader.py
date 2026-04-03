import os
from langchain_community.document_loaders import PyPDFLoader


def load_all_pdfs(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # ✅ Add metadata (VERY IMPORTANT)
            for doc in docs:
                doc.metadata["source"] = file

            documents.extend(docs)

    return documents