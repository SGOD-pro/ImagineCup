from app.ai.state import ClinicalGraphState
from app.ai.llm import NvidiaLLM
import json
from app.ai.prompts import REASONING_SYSTEM_PROMPT
from toon import encode


# -------------------------------
# Safety Filters (Deterministic)
# -------------------------------

CATASTROPHIC_CONDITIONS = {
    "leukemia",
    "leukaemia",
    "sepsis",
    "shock"
}


def drop_catastrophic_without_objective_support(h, signals) -> bool:
    """
    Catastrophic conditions MUST NOT appear unless
    there is objective physiological or hematologic support.
    """
    name = h.get("condition", "").lower()

    if any(c in name for c in CATASTROPHIC_CONDITIONS):
        if not (
            signals.get("hematologic_abnormality") or
            signals.get("physiological_instability")
        ):
            return False

    return True

def has_minimum_support(h):
    support = h.get("supporting_factors", [])
    contradictions = h.get("contradicting_factors", [])

    # MUST reference patient symptoms or labs
    patient_support = [
        s for s in support
        if "chief complaint" in s.lower()
        or "laboratory" in s.lower()
        or "lab" in s.lower()
        or "signal" in s.lower()
    ]

    if len(patient_support) == 0:
        return False

    if len(contradictions) >= len(patient_support):
        return False

    return True

def cap_confidence_by_signals(h, signals) -> None:
    """
    Confidence is strictly bounded by objective signals.
    """
    if (
        not signals.get("physiological_instability")
        and h.get("confidence") == "high"
    ):
        h["confidence"] = "medium"


# -------------------------------
# Reasoning Agent
# -------------------------------

def reasoning_agent(state: ClinicalGraphState) -> ClinicalGraphState:
    structured = state.get("structured_symptoms")
    lab_flags = state.get("lab_flags", {})
    evidence = state.get("evidence", [])
    clinical_signals = state.get("clinical_signals", {})

    if not structured:
        state["hypotheses"] = []
        return state

    prompt = f"""
You are a clinical reasoning assistant.

Your role is to suggest POSSIBLE CONDITIONS ONLY.
You must NOT assess urgency, severity, or risk level.

--------------------------------
Patient symptoms (structured):
{encode(json.dumps(structured, indent=2))}

Derived clinical signals (AUTHORITATIVE):
{encode(json.dumps(clinical_signals, indent=2))}

Laboratory findings (summarized):
{encode(json.dumps(lab_flags, indent=2))}

Retrieved medical evidence (CONTEXT ONLY, NOT AUTHORITATIVE):
{encode(json.dumps(evidence, indent=2))}
--------------------------------

HARD RULES (DO NOT VIOLATE):
1. Clinical signals OVERRIDE evidence text.
2. Do NOT infer severity, urgency, or risk.
3. If physiological_instability is FALSE, confidence MUST NOT be "high".
4. Do NOT propose catastrophic conditions without objective support.
5. If laboratory findings contradict a condition, list them explicitly.
6. If support is weak or indirect, lower confidence or OMIT the condition.
7. It is acceptable to return an empty list.

TASK:
Generate up to 3 POSSIBLE conditions to consider.

OUTPUT FORMAT (STRICT JSON):
[
  {{
    "condition": "<condition name>",
    "confidence": "low|medium|high",
    "supporting_factors": ["..."],
    "contradicting_factors": ["..."]
  }}
]
"""

    llm = NvidiaLLM(
        model_name="nvidia/llama-3.1-nemotron-ultra-253b-v1",
        temp=0.5
    )

    response = llm.model.invoke(
        REASONING_SYSTEM_PROMPT + "\n" + prompt
    )

    try:
        hypotheses = json.loads(str(response.content))
        if not isinstance(hypotheses, list):
            raise ValueError("Invalid reasoning output")

        filtered = []
        for h in hypotheses:
            # 1️⃣ Drop catastrophic without support
            if not drop_catastrophic_without_objective_support(h, clinical_signals):
                continue

            # 2️⃣ Enforce minimum epistemic support
            if not has_minimum_support(h):
                continue

            # 3️⃣ Cap confidence deterministically
            cap_confidence_by_signals(h, clinical_signals)

            filtered.append(h)

        state["hypotheses"] = filtered

    except Exception:
        state["hypotheses"] = []

    return state
