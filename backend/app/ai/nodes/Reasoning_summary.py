from app.ai.state import ClinicalGraphState

async def reasoning_summary_node(state: ClinicalGraphState) -> ClinicalGraphState:
    summary = {
        "high_confidence": [],
        "medium_confidence": []
    }

    for h in state.get("hypotheses", []):
        if h["confidence"] == "high":
            summary["high_confidence"].append(h["condition"])
        elif h["confidence"] == "medium":
            summary["medium_confidence"].append(h["condition"])

    state["reasoning_summary"] = summary
    return state
