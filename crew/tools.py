from crewai.tools import tool
from src.rag_pipeline import retrieve_context, format_context


@tool("Financial RAG Search Tool")
def financial_rag_search_tool(query: str) -> str:
    """
    Searches the FAISS financial knowledge base and returns relevant
    market reports, stock news, historical data, sector outlook, and risk commentary.
    """
    contexts = retrieve_context(query, k=4)
    return format_context(contexts)
