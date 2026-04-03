def retriever_agent(db, query):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    return context