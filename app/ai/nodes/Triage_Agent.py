from app.ai.state import ClinicalGraphState
from app.ai.llm import NVDIALLM
from app.helper.risk_rule_engine import determine_risk
def triage_agent(state: ClinicalGraphState) -> ClinicalGraphState:
     structured = state.get("structured_symptoms")
     labs = state.get("lab_results", [])

     if not structured:
          state["risk_level"] = "low"
          state["triage_rationale"] = "Insufficient structured information for risk assessment."
          state["escalation_required"] = False
          return state

     # --- Deterministic risk decision ---
     risk = determine_risk(structured, labs)
     escalation = risk == "critical"

     # --- LLM explanation ONLY ---
     llm = NVDIALLM(
          model_name="nvidia/llama-3.3-nemotron-super-49b-v1.5",
          temp=0.3
     )

     prompt = f"""
     You are a clinical triage explanation assistant.

     Risk level has already been determined as: {risk}

     Input data:
     Structured symptoms:
     {structured}

     Lab results:
     {labs}

     Task:
     Explain WHY this risk level was assigned.

     Rules:
     - Do NOT change the risk level
     - Do NOT provide diagnosis
     - Do NOT suggest treatment
     - Use cautious, professional language
     - 2–4 sentences max
     """

     explanation = llm.invoke(prompt).content

     state["risk_level"] = risk
     state["triage_rationale"] = str(explanation)
     state["escalation_required"] = escalation

     return state


