from app.ai.state import ClinicalGraphState

def clinical_signal_node(state: ClinicalGraphState) -> ClinicalGraphState:
    structured = state.get("structured_symptoms") or {}
    labs = state.get("lab_flags") or {}
    evidence = state.get("evidence") or []

    signals = {}

    # -------------------------------------------------
    # 1. Symptom-based signals
    # -------------------------------------------------
    chief = [c.lower() for c in structured.get("chief_complaints", [])]
    red_flags = [r.lower() for r in structured.get("red_flags", [])]

    signals["red_flag_present"] = len(red_flags) > 0

    signals["bleeding_present"] = any(
        kw in rf
        for rf in red_flags
        for kw in ["bleed", "blood", "black stool", "vomit blood"]
    )

    signals["neurological_symptoms"] = any(
        kw in " ".join(chief)
        for kw in ["confusion", "drowsy", "seizure", "unconscious"]
    )

    signals["respiratory_distress"] = any(
        kw in " ".join(chief)
        for kw in ["breath", "breathing", "shortness"]
    )

    signals["persistent_fever"] = any("fever" in c for c in chief)

    signals["severe_pain"] = any(
        kw in " ".join(chief)
        for kw in ["severe", "intense", "unbearable"]
    )

    # -------------------------------------------------
    # 2. Laboratory pattern signals (GENERIC)
    # -------------------------------------------------
    def lab_status(name):
        return labs.get(name, {}).get("status")

    def lab_value(name):
        return labs.get(name, {}).get("value")

    signals["anemia"] = (
        lab_status("haemoglobin") == "low"
    )

    hb = lab_value("haemoglobin")

    signals["severe_anemia"] = (
        lab_status("haemoglobin") == "low"
        and isinstance(hb, (int, float))
        and hb < 7
    )


    platelets = lab_value("platelet count")

    signals["thrombocytopenia"] = (
        lab_status("platelet count") == "low"
    )

    signals["severe_thrombocytopenia"] = (
        lab_status("platelet count") == "low"
        and isinstance(platelets, (int, float))
        and platelets < 100_000
    )

    signals["thrombocytosis"] = (
        lab_status("platelet count") == "high"
    )

    signals["microcytosis"] = (
        lab_status("mcv") == "low"
    )

    signals["macrocytosis"] = (
        lab_status("mcv") == "high"
    )

    signals["leukopenia"] = (
        lab_status("total wbc count") == "low"
    )

    signals["leukocytosis"] = (
        lab_status("total wbc count") == "high"
    )

    # -------------------------------------------------
    # 3. Guideline-derived signals (ABSTRACTED)
    # -------------------------------------------------
    signals["guideline_early_warning"] = any(
        e.get("signal_type") == "early_warning"
        for e in evidence
    )

    signals["guideline_severity"] = any(
        e.get("signal_type") == "severity"
        for e in evidence
    )

    signals["guideline_escalation"] = any(
        e.get("signal_type") == "escalation"
        for e in evidence
    )

    # -------------------------------------------------
    # 4. Physiological instability (THIS IS CRITICAL)
    # -------------------------------------------------
    signals["physiological_instability"] = any([
        signals["bleeding_present"],
        signals["severe_anemia"],
        signals["severe_thrombocytopenia"],
        signals["neurological_symptoms"],
        signals["respiratory_distress"],
    ])

    # -------------------------------------------------
    # 5. High-level pattern flags (triage-friendly)
    # -------------------------------------------------
    signals["hematologic_abnormality"] = any([
        signals["anemia"],
        signals["thrombocytopenia"],
        signals["thrombocytosis"],
        signals["microcytosis"],
        signals["macrocytosis"],
    ])

    signals["infection_like_pattern"] = any([
        signals["persistent_fever"],
        signals["guideline_early_warning"],
    ])

    state["clinical_signals"] = signals
    return state
