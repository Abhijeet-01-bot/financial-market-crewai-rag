def validate_retrieval(contexts, min_contexts: int = 2) -> dict:
    if not contexts:
        return {
            "valid": False,
            "message": "No relevant context retrieved."
        }

    if len(contexts) < min_contexts:
        return {
            "valid": False,
            "message": "Retrieved context is limited. Answer may be incomplete."
        }

    total_chars = sum(len(ctx["content"]) for ctx in contexts)

    if total_chars < 300:
        return {
            "valid": False,
            "message": "Retrieved context is too short for strong grounding."
        }

    return {
        "valid": True,
        "message": "Retrieved context is sufficient for grounded generation."
    }
