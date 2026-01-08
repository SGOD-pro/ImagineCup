def determine_risk(structured_symptoms, lab_flags):
    red_flags = [rf.lower() for rf in structured_symptoms.get("red_flags", [])]

    # -------------------------
    # 1. Physiological instability (CRITICAL)
    # -------------------------
    danger_symptoms = {
        "vomiting blood",
        "black stools",
        "seizures",
        "confusion",
        "drowsiness",
        "difficulty breathing",
        "hypotension",
    }

    unstable = False

    for rf in red_flags:
        if any(ds in rf for ds in danger_symptoms):
            unstable = True

    for name, lab in lab_flags.items():
        value = lab["value"]
        status = lab["status"]

        if name == "platelet count" and status == "low" and value < 100_000:
            unstable = True

        if name == "haemoglobin" and status == "low" and value < 7:
            unstable = True

    if unstable:
        return "critical"

    # -------------------------
    # 2. Objective concerning patterns (HIGH)
    # -------------------------
    objective_red_flags = {
        "bleeding",
        "vomiting blood",
        "black stools",
    }

    if any(any(obj in rf for obj in objective_red_flags) for rf in red_flags):
        return "high"

    # -------------------------
    # 3. Non-specific red flags or lab abnormalities (MEDIUM)
    # -------------------------
    if red_flags:
        return "medium"

    if any(lab["status"] in ("high", "low") for lab in lab_flags.values()):
        return "medium"

    # -------------------------
    # 4. Otherwise LOW
    # -------------------------
    return "low"
