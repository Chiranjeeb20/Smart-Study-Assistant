# 📘 Smart Study Assistant (RAG)

An AI-powered study assistant that allows users to upload PDFs and ask questions.
The system uses Retrieval-Augmented Generation (RAG) to provide answers grounded
in the uploaded documents, along with source references.

---

## 🚀 Features

- Upload one or multiple PDFs
- Ask questions based on uploaded documents
- Persistent FAISS vector storage
- Explainable answers with sources (PDF name & page)
- Streamlit-based chat UI
- FastAPI backend with Swagger documentation

---

## 🧠 Tech Stack

**Frontend**
- Streamlit

**Backend**
- FastAPI
- LangChain
- FAISS

**AI / NLP**
- SentenceTransformers (`all-MiniLM-L6-v2`)
- HuggingFace Transformers (FLAN-T5)

---

## 🏗️ Project Structure

```text
SSA/
├── backend/
│   ├── main.py
│   ├── pdf_loader.py
│   ├── vector_store.py
│   ├── rag_pipeline.py
│   └── __init__.py
├── frontend/
│   └── app.py
├── data/
│   └── uploaded PDFs
├── vector_db/
│   └── FAISS index
├── venv/
├── requirements.txt
└── README.md