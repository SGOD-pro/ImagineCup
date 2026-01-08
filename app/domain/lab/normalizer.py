from app.domain.lab.registry import LAB_REGISTRY
def normalize_labs(raw_tests: list[dict], context) -> list[dict]:
    normalized = []
    print("normalize_labs", context)
    sex = context.sex

    for t in raw_tests:
        name = t.get("name", "").lower()
        value = t.get("value")

        if name not in LAB_REGISTRY:
            normalized.append({
                "name": t.get("name"),
                "value": value,
                "unit": t.get("unit"),
                "status": "UNCLASSIFIED",
                "used_for_risk": False,
                "note": "Not used for automated triage"
            })
            continue

        ref = LAB_REGISTRY[name]
        ranges = ref["ranges"]

        low, high = (
            ranges.get(sex) if sex in ranges else ranges.get("all")
        )

        if value is None:
            status = "UNKNOWN"
        elif value < low:
            status = "LOW"
        elif value > high:
            status = "HIGH"
        else:
            status = "NORMAL"

        normalized.append({
            "name": t.get("name"),
            "value": value,
            "unit": ref["unit"],
            "reference_low": low,
            "reference_high": high,
            "status": status,
            "used_for_risk": True
        })

    return normalized
