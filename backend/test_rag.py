from pdf_loader import load_pdf
from vector_store import create_vector_store
from rag_pipeline import get_qa_chain

docs = load_pdf("data/java.pdf")

db = create_vector_store(docs)
qa = get_qa_chain(db)

query = "Summarize this document in simple terms"
result = qa(query)

print("\nQUESTION:", query)
print("ANSWER:", result["result"])