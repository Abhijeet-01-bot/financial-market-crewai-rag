from src.rag_pipeline import retrieve_context


def keyword_score(query: str, text: str) -> int:
    query_terms = [
        word.lower().strip(".,?:;")
        for word in query.split()
        if len(word) > 3
    ]

    text_lower = text.lower()

    return sum(1 for term in query_terms if term in text_lower)


def hybrid_retrieve(query: str, k: int = 4):
    semantic_results = retrieve_context(query, k=8)

    reranked = sorted(
        semantic_results,
        key=lambda item: keyword_score(query, item["content"]),
        reverse=True
    )

    return reranked[:k]


if __name__ == "__main__":
    query = "banking IT risk volatility portfolio"
    results = hybrid_retrieve(query)

    for result in results:
        print(result["source"])
        print(result["content"][:500])
        print("-" * 80)
