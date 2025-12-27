from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def get_qa_chain(vector_db):
    hf_pipeline = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_new_tokens=300
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an academic study assistant.

Rules:
- Answer ONLY using the context below.
- Be concise and structured.
- Use bullet points if helpful.
- If the answer is not found in the context, say:
  "The document does not provide this information."

Context:
{context}

Question:
{question}

Answer:
"""
)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever = vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # was 3–4 earlier
        )
    )

    return qa_chain