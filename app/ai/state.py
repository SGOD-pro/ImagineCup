# from typing_extensions import TypedDict

# class ClinicalGraphState(TypedDict):
#     raw_symptoms_text: str
#     patient_age: int
#     patient_gender: str
#     lab_results: list

#     structured_symptoms: dict | None
#     evidence: list
#     hypotheses: list
#     risk_level: str | None
#     triage_rationale: str|None
#     escalation_required: bool


from typing_extensions import TypedDict
from typing import Optional, List, Dict, Any


class ClinicalGraphState(TypedDict):
    # raw input
    raw_symptoms_text: str
    patient_age: int
    patient_gender: str
    lab_results: List[Dict[str, Any]]

    # agents
    structured_symptoms: Optional[Dict[str, Any]]
    evidence: List[Dict[str, Any]]

    clinical_signals: Dict[str, Any]
    
    # deterministic derived data
    lab_flags: Dict[str, Dict[str, Any]]
    reasoning_summary: Dict[str, Any]

    # reasoning + triage
    hypotheses: List[Dict[str, Any]]
    risk_level: Optional[str]
    triage_rationale: Optional[str]
    escalation_required: bool

    # safety
    safety_notes: Optional[str]
