import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.data_loader import load_documents


def build_vector_store():
    raw_docs = load_documents("data/raw")

    if not raw_docs:
        raise ValueError("No documents found in data/raw. Please run fetch_web_financial_data.py first.")

    documents = []

    for item in raw_docs:
        documents.append(
            Document(
                page_content=item["content"],
                metadata={"source": item["source"]}
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("vectorstore/faiss_index", exist_ok=True)

    vectorstore.save_local("vectorstore/faiss_index")

    print("FAISS vector store created successfully")
    print(f"Total documents loaded: {len(documents)}")
    print(f"Total chunks stored: {len(chunks)}")


if __name__ == "__main__":
    build_vector_store()
