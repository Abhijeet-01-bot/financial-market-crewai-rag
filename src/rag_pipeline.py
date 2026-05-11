from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


FAISS_INDEX_PATH = "vectorstore/faiss_index"


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_context(query: str, k: int = 4):
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(query, k=k)

    contexts = []

    for doc in docs:
        contexts.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown")
        })

    return contexts


def format_context(contexts):
    formatted_text = ""

    for i, ctx in enumerate(contexts, start=1):
        formatted_text += f"\nSource {i}: {ctx['source']}\n"
        formatted_text += f"{ctx['content']}\n"
        formatted_text += "-" * 80
        formatted_text += "\n"

    return formatted_text


if __name__ == "__main__":
    test_query = "What is the risk outlook for banking and IT stocks?"

    print("Query:")
    print(test_query)

    print("\nRetrieved Context:")
    results = retrieve_context(test_query, k=4)

    print(format_context(results))
