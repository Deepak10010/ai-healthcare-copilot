import streamlit as st
import requests

st.set_page_config(page_title="AI Healthcare Copilot", page_icon="🩺", layout="centered")

st.title("AI Healthcare Copilot")

query = st.text_input("Ask a healthcare question:")

if st.button("Submit"):
    if query.strip():
        try:
            response = requests.post(
                "http://backend:8000/ask",
                json={"query": query},
                timeout=180
            )

            data = response.json()

            st.subheader("Raw API response:")
            st.json(data)

            if isinstance(data, dict):
                if data.get("status") == "success":
                    st.subheader("Answer:")
                    st.write(data.get("answer", "No answer returned"))
                else:
                    st.error(data.get("error", "Unknown backend error"))
                    if data.get("traceback"):
                        with st.expander("Traceback"):
                            st.code(data["traceback"])
            else:
                st.error(f"Unexpected response: {data}")

        except Exception as e:
            st.error(f"Frontend request failed: {e}")