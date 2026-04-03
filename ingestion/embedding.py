# Converts meaning into numbers

# from langchain_openai import OpenAIEmbeddings

# def get_embeddings():
#     return OpenAIEmbeddings()


from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")