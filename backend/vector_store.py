import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DB_PATH = "vector_db/faiss_index"


def create_or_load_vector_store(documents=None):
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # ✅ Case 1: FAISS already exists → just load it
    if os.path.exists(VECTOR_DB_PATH):
        print("🔁 Loading existing FAISS index from disk...")
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # ✅ Case 2: No FAISS yet AND no documents
    if documents is None:
        print("⚠️ No existing vector DB and no documents provided.")
        return None

    # ✅ Case 3: Create new FAISS from documents
    print("🆕 Creating new FAISS index...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)

    return vector_db