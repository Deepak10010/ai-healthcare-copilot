from langchain_openai import ChatOpenAI

def ask_question(db, query):
    retriever = db.as_retriever()

    docs = retriever.get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(model="gpt-4")

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.predict(prompt)

    return response