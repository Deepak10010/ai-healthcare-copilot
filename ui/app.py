import os

import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(
    page_title="AI Healthcare Copilot",
    page_icon="🩺",
    layout="wide",
)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


# --- Helper Functions ---
def create_session():
    """Create a new backend session and return the session_id."""
    try:
        resp = requests.post(f"{BACKEND_URL}/session", timeout=10)
        return resp.json().get("session_id")
    except Exception:
        return None


def get_health():
    """Fetch backend health status."""
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=10)
        return resp.json()
    except Exception:
        return None


def ask_question(query: str, session_id: str = None):
    """Send a query to the backend and return the response."""
    payload = {"query": query}
    if session_id:
        payload["session_id"] = session_id
    resp = requests.post(
        f"{BACKEND_URL}/ask",
        json=payload,
        timeout=180,
    )
    return resp.json()


def upload_file(uploaded_file):
    """Upload a document to the backend for indexing."""
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    resp = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
    return resp.json()


# --- Session State Init ---
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()
    st.session_state.messages = []


# --- Sidebar ---
with st.sidebar:
    st.header("🩺 System Info")

    health = get_health()
    if health:
        st.metric("Status", health.get("status", "unknown"))
        st.metric("LLM Model", health.get("model", "N/A"))
        st.metric("Embedding Model", health.get("embedding_model", "N/A"))
        st.metric("Documents Indexed", health.get("documents_indexed", 0))

        col1, col2 = st.columns(2)
        with col1:
            re_rank = "On" if health.get("rerank_enabled") else "Off"
            st.metric("Re-ranking", re_rank)
        with col2:
            router = "On" if health.get("router_enabled") else "Off"
            st.metric("Query Router", router)
    else:
        st.error("Backend unavailable")

    st.divider()

    # --- Document Upload ---
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Add a document to the knowledge base",
        type=["pdf", "txt", "docx"],
    )
    if uploaded_file and st.button("Upload & Index"):
        with st.spinner("Uploading and indexing..."):
            try:
                result = upload_file(uploaded_file)
                if result.get("status") == "success":
                    st.success(
                        f"Indexed **{uploaded_file.name}** "
                        f"({result.get('chunks_created', 0)} chunks)"
                    )
                else:
                    st.error(result.get("detail", "Upload failed"))
            except Exception as e:
                st.error(f"Upload failed: {e}")

    st.divider()

    # --- New Conversation ---
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.session_id = create_session()
        st.session_state.messages = []
        st.rerun()

    st.caption(f"Session: {st.session_state.session_id[:8] if st.session_state.session_id else 'N/A'}...")


# --- Main Chat Interface ---
st.title("🩺 AI Healthcare Copilot")
st.caption("Ask questions about medical documents — powered by RAG with multi-agent AI")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Show sources for assistant messages
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 Sources"):
                for src in msg["sources"]:
                    page = src.get("page")
                    page_text = f", Page {page + 1}" if page is not None else ""
                    st.caption(f"📄 {src['document']}{page_text}")

        # Show metadata for assistant messages
        if msg["role"] == "assistant" and msg.get("query_type"):
            cols = st.columns(3)
            with cols[0]:
                st.caption(f"Type: {msg.get('query_type', 'N/A')}")
            with cols[1]:
                score = msg.get("score", 0)
                st.caption(f"Confidence: {score}/10")
            with cols[2]:
                timing = msg.get("total_time")
                if timing:
                    st.caption(f"Time: {timing:.1f}s")

# Chat input
if prompt := st.chat_input("Ask a healthcare question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            try:
                data = ask_question(prompt, st.session_state.session_id)

                if data.get("status") == "success":
                    answer = data.get("answer", "No answer returned")
                    sources = data.get("sources", [])
                    score = data.get("score", 0)
                    query_type = data.get("query_type", "N/A")
                    timing = data.get("timing", {})
                    total_time = sum(timing.values()) if timing else None

                    st.markdown(answer)

                    if sources:
                        with st.expander("📚 Sources"):
                            for src in sources:
                                page = src.get("page")
                                page_text = f", Page {page + 1}" if page is not None else ""
                                st.caption(f"📄 {src['document']}{page_text}")

                    cols = st.columns(3)
                    with cols[0]:
                        st.caption(f"Type: {query_type}")
                    with cols[1]:
                        st.caption(f"Confidence: {score}/10")
                    with cols[2]:
                        if total_time:
                            st.caption(f"Time: {total_time:.1f}s")

                    # Store in session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "score": score,
                        "query_type": query_type,
                        "total_time": total_time,
                    })
                else:
                    error_msg = data.get("message", "Something went wrong")
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {error_msg}",
                    })

            except Exception as e:
                st.error(f"Request failed: {e}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {e}",
                })
