# from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

def ask_question(db, query):

    # Finds relevant info
    retriever = db.as_retriever() 

    # docs = retriever.get_relevant_documents(query)
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    # llm = ChatOpenAI(model="gpt-4") 
    # Explains answer
    llm = Ollama(model="llama3")

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    return response