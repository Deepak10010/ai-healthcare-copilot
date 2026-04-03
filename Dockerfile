FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi uvicorn streamlit requests \
    langchain langchain-community faiss-cpu pypdf

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]