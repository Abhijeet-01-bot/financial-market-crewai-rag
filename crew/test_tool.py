from crew.tools import financial_rag_search_tool

if __name__ == "__main__":
    result = financial_rag_search_tool.run(
        "What is the risk outlook for banking and IT stocks?"
    )
    print(result)
