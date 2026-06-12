from fastapi import FastAPI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import pipeline
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

vector_store = Chroma(persist_directory="./nutrition_chroma", embedding_function=embedding_model)

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 8, "fetch_k": 20})

pipe = pipeline("text-generation", model="Qwen/Qwen2.5-7B-Instruct")

@app.post("/ask")
def ask(req: QueryRequest):

    docs = retriever.invoke(req.question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
        You are a nutrition research assistant. If you can't answer the question given the context, say "I don't know".

        Context: 
        {context}

        Question: 
        {req.question}

        Answer: 
    """
    output = pipe(prompt, max_new_tokens=30, do_sample=False)
    answer = output[0]["generated_text"]

    return {
        "answer": answer,
        "sources": [
            doc.metadata.get("source", "unknown")
            for doc in docs
        ]
    }
