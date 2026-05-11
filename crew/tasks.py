from crewai import Task

from crew.agents import (
    retriever_agent,
    analysis_agent,
    risk_agent,
    portfolio_agent
)


def create_tasks(query: str, risk_appetite: str):
    retrieval_task = Task(
        description=(
            f"User query: {query}\n\n"
            "Use the Financial RAG Search Tool to retrieve relevant financial context. "
            "Return the most important evidence with source names. "
            "Do not generate final analysis yet."
        ),
        expected_output=(
            "A structured list of retrieved financial evidence with source names. "
            "Include relevant data from market reports, stock news, historical data, "
            "sector outlook, or risk commentary."
        ),
        agent=retriever_agent
    )

    analysis_task = Task(
        description=(
            f"Analyze the retrieved financial context for this query:\n{query}\n\n"
            "Generate grounded financial market intelligence using only retrieved evidence. "
            "Do not invent unsupported financial facts."
        ),
        expected_output=(
            "A structured market analysis containing:\n"
            "1. Market/Sector Trend\n"
            "2. Key Evidence\n"
            "3. Sector or Stock Outlook\n"
            "4. Limitations\n"
            "5. Final Summary"
        ),
        agent=analysis_agent,
        context=[retrieval_task]
    )

    risk_task = Task(
        description=(
            "Using the retrieved context and market analysis, evaluate risk. "
            "Discuss volatility, downside risk, concentration risk, sector exposure, "
            "and overall risk level."
        ),
        expected_output=(
            "A structured risk assessment containing:\n"
            "1. Risk Level: Low/Medium/High\n"
            "2. Volatility Factors\n"
            "3. Concentration Risk\n"
            "4. Downside Risks\n"
            "5. Risk Summary"
        ),
        agent=risk_agent,
        context=[retrieval_task, analysis_task]
    )

    portfolio_task = Task(
        description=(
            f"Create an educational portfolio allocation for a user with "
            f"{risk_appetite} risk appetite.\n\n"
            "Use the market analysis and risk assessment. "
            "Provide allocation percentages. "
            "The allocation must total 100%. "
            "Include a clear disclaimer that this is educational only and not financial advice."
        ),
        expected_output=(
            "A portfolio allocation with percentages, reasoning, risk suitability, "
            "and disclaimer. Allocation must total 100%."
        ),
        agent=portfolio_agent,
        context=[analysis_task, risk_task]
    )

    return [
        retrieval_task,
        analysis_task,
        risk_task,
        portfolio_task
    ]
