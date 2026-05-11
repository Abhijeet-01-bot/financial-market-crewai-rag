from src.rag_pipeline import retrieve_context


def test_retrieve_context():
    results = retrieve_context("banking IT risk", k=2)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "content" in results[0]
    assert "source" in results[0]
