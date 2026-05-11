from dotenv import load_dotenv
from crewai import Crew, Process

from crew.agents import (
    retriever_agent,
    analysis_agent,
    risk_agent,
    portfolio_agent
)

from crew.tasks import create_tasks

load_dotenv(dotenv_path=".env")


def run_financial_crew(query: str, risk_appetite: str = "medium"):
    tasks = create_tasks(
        query=query,
        risk_appetite=risk_appetite
    )

    financial_crew = Crew(
        agents=[
            retriever_agent,
            analysis_agent,
            risk_agent,
            portfolio_agent
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "risk_appetite": risk_appetite
        }
    )

    return str(result)


if __name__ == "__main__":
    query = (
        "Analyze the outlook for banking and IT stocks and suggest "
        "a portfolio for a medium risk investor."
    )

    output = run_financial_crew(
        query=query,
        risk_appetite="medium"
    )

    print("\n\nFINAL CREW OUTPUT")
    print("=" * 80)
    print(output)
