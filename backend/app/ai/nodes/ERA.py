from app.ai.state import ClinicalGraphState
from app.ai.vector_search import similarity_search

"""
Evidence Retrieval Agent

- NO reasoning
- NO diagnosis
- Retrieves typed, cited clinical signals
"""

async def evidence_retrieval(state: ClinicalGraphState) -> ClinicalGraphState:
    structured = state.get("structured_symptoms")

    if not structured:
        state["evidence"] = []
        return state

    chief = structured.get("chief_complaints", [])
    red_flags = structured.get("red_flags", [])

    # build query
    query_parts = chief + red_flags
    query = " ".join(query_parts)

    # red flags bias escalation
    signal_types = ["early_warning", "severity"]
    if red_flags:
        signal_types.append("escalation")

    docs = await similarity_search(
        query=query,
        limit=5,
        signal_types=signal_types,
    )

    evidence = []
    for doc, score in docs:
        evidence.append({
            "statement": doc.page_content,
            "signal_type": doc.metadata.get("signal_type"),
            "symptoms": doc.metadata.get("symptoms"),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "score": round(score, 3),
        })

    state["evidence"] = evidence
    return state
