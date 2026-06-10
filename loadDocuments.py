from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pathlib import Path

documents = []

for pdf in Path("PDFs").glob("*.pdf"):
    loader = PyPDFLoader(str(pdf))
    documents.extend(loader.load())

print("PDFs loaded")

embeddingModel = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

chunks = text_splitter.split_documents(documents)

print("text split")

vector_store = Chroma(
    embedding_function=embeddingModel,
    persist_directory="./nutrition_chroma"
)

print("create vector db")

vector_store.add_documents(chunks)

print("added to vector db")

vector_store.persist()
