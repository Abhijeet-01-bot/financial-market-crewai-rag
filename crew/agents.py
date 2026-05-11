import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from crew.tools import financial_rag_search_tool

load_dotenv(dotenv_path=".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini/gemini-1.5-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

gemini_llm = LLM(
    model=LLM_MODEL,
    api_key=GEMINI_API_KEY,
    temperature=0.2
)


retriever_agent = Agent(
    role="Financial Market Retriever Agent",
    goal=(
        "Retrieve relevant financial market reports, stock news, historical data, "
        "sector outlook, and risk commentary for the user's query."
    ),
    backstory=(
        "You are a financial data retrieval specialist. "
        "You use the Financial RAG Search Tool to collect grounded context from FAISS."
    ),
    tools=[financial_rag_search_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)


analysis_agent = Agent(
    role="Financial Market Analysis Agent",
    goal="Generate grounded financial market intelligence using retrieved context.",
    backstory=(
        "You are a senior financial market analyst. "
        "You analyze sector trends, stock movement, and market sentiment using only retrieved evidence."
    ),
    tools=[financial_rag_search_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)


risk_agent = Agent(
    role="Risk Assessment Agent",
    goal=(
        "Evaluate volatility, downside risk, concentration risk, and portfolio exposure "
        "based on retrieved financial context."
    ),
    backstory=(
        "You are a financial risk analyst. "
        "You identify volatility, sector exposure, drawdown possibility, and risk level."
    ),
    tools=[financial_rag_search_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)


portfolio_agent = Agent(
    role="Portfolio Allocation Agent",
    goal=(
        "Suggest an educational portfolio allocation based on risk appetite, market analysis, "
        "and risk assessment."
    ),
    backstory=(
        "You are a portfolio strategy assistant. "
        "You create educational allocations and always include a disclaimer that this is not financial advice."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)
