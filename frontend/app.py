import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Smart Study Assistant",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Smart Study Assistant (RAG)")
st.write("Chat with your PDFs using AI")

# -----------------------------
# Sidebar - PDF Upload
# -----------------------------
with st.sidebar:
    st.header("📤 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

if uploaded_file is not None:
    with st.spinner("Uploading and processing PDF..."):
        response = requests.post(
            f"{BACKEND_URL}/upload_pdf",
            files={"file": uploaded_file}
        )

    if response.status_code == 200:
        st.success("✅ PDF uploaded and processed successfully!")
    else:
        st.error("❌ Failed to upload PDF")

# -----------------------------
# Chat History Setup
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.header("💬 Ask Questions")

query = st.text_input("Enter your question")

col1, col2 = st.columns([1, 1])

with col1:
    ask_clicked = st.button("Ask")

with col2:
    clear_clicked = st.button("Clear Chat")

# Clear chat
if clear_clicked:
    st.session_state.chat_history = []
    st.success("Chat cleared")

# Ask question
if ask_clicked:
    if query.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            response = requests.get(
                f"{BACKEND_URL}/ask",
                params={"query": query}
            )

        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])

            st.session_state.chat_history.append(
                {
                    "question": query,
                    "answer": answer,
                    "sources": sources
                }
            )
        else:
            st.error("Error getting answer")

# -----------------------------
# Display Chat History
# -----------------------------
st.divider()
st.subheader("📜 Conversation")

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑 You:** {chat['question']}")
    st.markdown(f"**🤖 Assistant:** {chat['answer'][:800]}")

    if chat.get("sources"):
        with st.expander("📚 Sources used"):
            for src in chat["sources"]:
                st.markdown(
                    f"""
**File:** {src['source']}  
**Page:** {src['page']}  
**Snippet:** {src['content']}
---
"""
                )