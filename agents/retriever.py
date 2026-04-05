def retriever_agent(db, query: str) -> str:
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    context = "\n\n".join(doc.page_content for doc in docs)
    return context[:2500]