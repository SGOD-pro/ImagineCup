def determine_risk(structured, labs):
    red_flags = structured.get("red_flags", [])
    if red_flags:
        return "critical"

    for lab in labs:
        if lab.get("status") == "HIGH":
            # crude but explainable
            if lab["name"].lower() in ["total bilirubin", "direct bilirubin"]:
                return "critical"

    duration = structured.get("duration")
    if duration and any(word in duration.lower() for word in ["week", "weeks"]):
        return "medium"

    return "low"
