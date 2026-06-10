from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pathlib import Path

documents = []

for pdf in Path("PDFs").glob("*.pdf"):
    loader = PyPDFLoader(str(pdf))
    documents.extend(loader.load())

embeddingModel = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

text_splitter = SemanticChunker(embeddingModel, breakpoint_threshold_type="percentile")

chunks = text_splitter.split_documents(documents)

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddingModel,
    persist_directory="./nutrition_chroma"
)

vector_store.persist()
