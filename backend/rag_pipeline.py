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
You are a smart study assistant.
Answer the question ONLY using the given context.
If the answer is not present in the context, say "I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer (clear and student-friendly):
"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True  # 🔥 IMPORTANT
    )

    return qa_chain