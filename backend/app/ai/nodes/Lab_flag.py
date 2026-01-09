from app.ai.graph import ClinicalGraphState

async def lab_flag_node(state: ClinicalGraphState) -> ClinicalGraphState:
    flags = {}

    for lab in state.get("lab_results", []):
        name = lab.get("name")
        value = lab.get("value")
        low = lab.get("reference_low")
        high = lab.get("reference_high")

        if not name or value is None or low is None or high is None:
            continue  # ignore OCR garbage safely

        status = (
            "low" if value < low else
            "high" if value > high else
            "normal"
        )

        flags[name.lower()] = {
            "value": value,
            "low": low,
            "high": high,
            "status": status
        }

    state["lab_flags"] = flags
    return state
