import os
import pandas as pd
from datetime import datetime

from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from src.baseline_rag import run_baseline_rag
from src.rag_pipeline import retrieve_context
from crew.crew_runner import run_financial_crew


def calculate_bleu(reference: str, generated: str) -> float:
    reference_tokens = [reference.lower().split()]
    generated_tokens = generated.lower().split()

    smoothie = SmoothingFunction().method4

    score = sentence_bleu(
        reference_tokens,
        generated_tokens,
        smoothing_function=smoothie
    )

    return round(score, 4)


def calculate_rouge(reference: str, generated: str) -> dict:
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"],
        use_stemmer=True
    )

    scores = scorer.score(reference, generated)

    return {
        "rouge1": round(scores["rouge1"].fmeasure, 4),
        "rouge2": round(scores["rouge2"].fmeasure, 4),
        "rougeL": round(scores["rougeL"].fmeasure, 4)
    }


def calculate_relevance_score(query: str, k: int = 4) -> float:
    """
    Lightweight relevance score:
    Checks how many important query terms appear in retrieved chunks.
    """

    contexts = retrieve_context(query, k=k)

    query_terms = set(
        word.lower().strip(".,?:;")
        for word in query.split()
        if len(word) > 3
    )

    if not query_terms:
        return 0.0

    relevance_scores = []

    for ctx in contexts:
        content = ctx["content"].lower()
        matched_terms = [term for term in query_terms if term in content]
        score = len(matched_terms) / len(query_terms)
        relevance_scores.append(score)

    if not relevance_scores:
        return 0.0

    return round(sum(relevance_scores) / len(relevance_scores), 4)


def run_evaluation():
    os.makedirs("evaluation_results", exist_ok=True)

    test_cases = [
        {
            "query": "Analyze banking and IT sector outlook for a medium risk investor.",
            "risk_appetite": "medium",
            "reference_answer": (
                "Banking sector has a mixed or neutral outlook with medium risk. "
                "The IT sector has a weak outlook with medium volatility. "
                "A medium risk investor should diversify across banking, IT, defensive sectors, "
                "large-cap exposure, and cash while avoiding concentration risk."
            )
        },
        {
            "query": "What are the main risks in banking and IT stocks?",
            "risk_appetite": "medium",
            "reference_answer": (
                "Main risks include volatility, negative one-year returns, sector concentration, "
                "downside risk, and uncertainty in banking and information technology stocks."
            )
        },
        {
            "query": "Suggest portfolio allocation for a low risk investor.",
            "risk_appetite": "low",
            "reference_answer": (
                "A low risk investor should prefer lower-volatility large-cap exposure, "
                "defensive sectors, diversified index funds, cash allocation, and avoid "
                "high concentration in volatile sectors."
            )
        }
    ]

    results = []

    for case in test_cases:
        query = case["query"]
        risk_appetite = case["risk_appetite"]
        reference = case["reference_answer"]

        print(f"\nEvaluating query: {query}")

        baseline_answer = run_baseline_rag(query)

        try:
            agentic_answer = run_financial_crew(
                query=query,
                risk_appetite=risk_appetite
            )
        except Exception as e:
            agentic_answer = f"Agentic RAG failed due to error: {str(e)}"

        baseline_bleu = calculate_bleu(reference, baseline_answer)
        agentic_bleu = calculate_bleu(reference, agentic_answer)

        baseline_rouge = calculate_rouge(reference, baseline_answer)
        agentic_rouge = calculate_rouge(reference, agentic_answer)

        relevance_score = calculate_relevance_score(query)

        results.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "risk_appetite": risk_appetite,

            "baseline_bleu": baseline_bleu,
            "agentic_bleu": agentic_bleu,

            "baseline_rouge1": baseline_rouge["rouge1"],
            "baseline_rouge2": baseline_rouge["rouge2"],
            "baseline_rougeL": baseline_rouge["rougeL"],

            "agentic_rouge1": agentic_rouge["rouge1"],
            "agentic_rouge2": agentic_rouge["rouge2"],
            "agentic_rougeL": agentic_rouge["rougeL"],

            "retrieval_relevance_score": relevance_score,

            "baseline_answer": baseline_answer,
            "agentic_answer": agentic_answer
        })

    df = pd.DataFrame(results)

    output_path = "evaluation_results/evaluation_report.csv"
    df.to_csv(output_path, index=False)

    print("\nEvaluation completed.")
    print(f"Results saved to: {output_path}")

    print(
        df[
            [
                "query",
                "baseline_bleu",
                "agentic_bleu",
                "baseline_rouge1",
                "agentic_rouge1",
                "retrieval_relevance_score"
            ]
        ]
    )


if __name__ == "__main__":
    run_evaluation()
