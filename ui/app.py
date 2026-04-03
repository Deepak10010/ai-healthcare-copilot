import streamlit as st
import requests

st.title("🧠 AI Healthcare Copilot")

query = st.text_input("Ask a question")

if st.button("Ask"):
    if query:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"query": query}
        )
        answer = response.json()["answer"]

        st.subheader("Answer:")
        st.write(answer)