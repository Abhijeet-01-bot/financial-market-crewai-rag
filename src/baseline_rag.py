from src.rag_pipeline import retrieve_context, format_context


def run_baseline_rag(query: str) -> str:
    contexts = retrieve_context(query, k=4)
    formatted_context = format_context(contexts)

    answer = f"""
Baseline RAG Answer:

Retrieved Context:
{formatted_context}

Summary:
This baseline answer is generated directly from retrieved context.
It does not use multiple agents, task delegation, risk analysis, or portfolio specialization.
"""

    return answer


if __name__ == "__main__":
    query = "Analyze banking and IT sector outlook for a medium risk investor."
    print(run_baseline_rag(query))
