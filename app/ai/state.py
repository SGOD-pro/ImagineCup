from typing_extensions import TypedDict

class ClinicalGraphState(TypedDict):
    raw_symptoms_text: str
    patient_age: int
    patient_gender: str
    lab_results: list

    structured_symptoms: dict | None
    evidence: list
    hypotheses: list
    risk_level: str | None
    triage_rationale: str|None
    escalation_required: bool
