from fastapi import FastAPI
from api.schemas import QueryRequest, QueryResponse
from crew.crew_runner import run_financial_crew

app = FastAPI(
    title="Financial Market Intelligence CrewAI RAG API",
    description="CrewAI multi-agent RAG system for financial market intelligence.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Financial Market Intelligence CrewAI RAG API is running"
    }


@app.post("/query", response_model=QueryResponse)
def query_financial_agent(request: QueryRequest):
    result = run_financial_crew(
        query=request.query,
        risk_appetite=request.risk_appetite
    )

    return QueryResponse(
        query=request.query,
        risk_appetite=request.risk_appetite,
        response=result
    )
