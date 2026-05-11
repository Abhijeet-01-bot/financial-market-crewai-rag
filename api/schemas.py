from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    risk_appetite: str = "medium"


class QueryResponse(BaseModel):
    query: str
    risk_appetite: str
    response: str
