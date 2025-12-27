from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.pdf_loader import load_pdf
from backend.vector_store import create_or_load_vector_store
from backend.rag_pipeline import get_qa_chain

app = FastAPI(title="Smart Study Assistant (RAG)")

VECTOR_DB = None


@app.on_event("startup")
def load_vector_db_on_startup():
    global VECTOR_DB
    VECTOR_DB = create_or_load_vector_store()
    if VECTOR_DB:
        print("✅ Vector DB loaded on startup")
    else:
        print("ℹ️ No vector DB found on startup")


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global VECTOR_DB

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_pdf(file_path)

    # If vector DB exists → add documents
    if VECTOR_DB:
        VECTOR_DB.add_documents(documents)
        VECTOR_DB.save_local("vector_db/faiss_index")
    else:
        VECTOR_DB = create_or_load_vector_store(documents)

    return {
        "message": "PDF processed and added successfully",
        "filename": file.filename
    }


@app.get("/ask")
async def ask_question(query: str):
    global VECTOR_DB

    if VECTOR_DB is None:
        return {
            "error": "No documents loaded yet. Please upload a PDF first."
        }

    try:
        qa_chain = get_qa_chain(VECTOR_DB)
        result = qa_chain(query)

        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A"),
                "content": doc.page_content[:300]
            })

        return {
            "question": query,
            "answer": result.get("result", ""),
            "sources": sources
        }

    except Exception as e:
        return {
            "error": "Failed to generate answer",
            "details": str(e)
        }