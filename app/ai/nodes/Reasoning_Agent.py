from app.ai.state import ClinicalGraphState
from app.ai.llm import NVDIALLM
import json
from app.ai.promts import REASONING_SYSTEM_PROMPT

def reasoning_agent(state: ClinicalGraphState) -> ClinicalGraphState:
    structured = state.get("structured_symptoms")
    labs = state.get("lab_results", [])
    evidence = state.get("evidence", [])

    if not structured:
        state["hypotheses"] = []
        return state

    prompt = f"""
Symptoms:
{json.dumps(structured, indent=2)}

Lab Results:
{json.dumps(labs, indent=2)}

Medical Evidence:
{json.dumps(evidence, indent=2)}

Task:
Generate a list of possible conditions to consider.

Output JSON schema:
[
  {{
    "condition": "<condition name>",
    "supporting_factors": ["..."],
    "contradicting_factors": ["..."]
  }}
]

Constraints:
- Maximum 3 conditions
- Use cautious, non-diagnostic language
- If evidence is insufficient, return an empty list
"""

    llm = NVDIALLM(
        model_name="nvidia/llama-3.1-nemotron-ultra-253b-v1",
        temp=0.4
    )

    response = llm.invoke(
        REASONING_SYSTEM_PROMPT + "\n" + prompt
    )

    try:
        hypotheses = json.loads(str(response.content))
        if not isinstance(hypotheses, list):
            raise ValueError("Invalid reasoning output")
    except Exception:
        hypotheses = []

    state["hypotheses"] = hypotheses
    return state
