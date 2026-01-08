from app.ai.state import ClinicalGraphState

async def guardrail_node(state: ClinicalGraphState) -> ClinicalGraphState:
    notes = []

    # Language safety
    notes.append(
        "This system provides clinical decision support only and does not diagnose."
    )

    # Catastrophic suppression
    for h in state.get("hypotheses", []):
        if h["confidence"] == "low":
            notes.append(
                f"{h['condition']} is considered low confidence and requires further evaluation before concern."
            )

    # Escalation sanity
    if state["risk_level"] == "critical" and not state["escalation_required"]:
        state["risk_level"] = "high"
        notes.append("Risk adjusted after safety review.")

    state["safety_notes"] = " ".join(notes)
    return state
