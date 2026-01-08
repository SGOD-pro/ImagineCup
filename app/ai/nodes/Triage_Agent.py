from app.ai.state import ClinicalGraphState
from app.ai.llm import NvidiaLLM
from app.domain.lab.risk_engine import determine_risk
from toon import encode

def triage_agent(state: ClinicalGraphState) -> ClinicalGraphState:
     structured = state.get("structured_symptoms")
     lab_flags = state.get("lab_flags", {})
     summary = state.get("reasoning_summary", {})
     signals = state.get("clinical_signals", {})

     if not structured:
          state["risk_level"] = "low"
          state["escalation_required"] = False
          state["triage_rationale"] = "Insufficient information to determine clinical risk."
          return state

     # --- Deterministic risk decision ---
     risk = determine_risk(structured, lab_flags)
     escalation = risk == "critical"

     # --- LLM explanation ONLY ---
     llm = NvidiaLLM(
          model_name="nvidia/llama-3.3-nemotron-super-49b-v1.5",
          temp=0.3
     )

     prompt = f"""
You are a clinical triage explanation assistant.

The risk level has ALREADY been determined as: {risk}

Authoritative clinical signals:
{encode(signals)}

Context:
Structured symptoms:
{encode(structured)}

Laboratory patterns:
{encode(lab_flags)}

Reasoning summary:
{encode(summary)}

TASK:
Explain WHY this risk level was assigned.

LANGUAGE CONSTRAINTS (MANDATORY):
- If risk != "critical", you MUST NOT use words like:
  "life-threatening", "immediate danger", "critical condition"
- If physiological_instability is FALSE, avoid alarmist language.
- If risk == "critical", explain escalation clearly and calmly.

RULES:
- Do NOT change the risk level
- Do NOT provide diagnosis
- Do NOT suggest treatment
- Do NOT reinterpret raw lab values
- Use cautious, professional language
- 2–4 sentences maximum
"""

     explanation = llm.model.invoke(prompt).content
     explanation = str(explanation)
     # --- Deterministic post-check (important) ---
     if not signals.get("physiological_instability"):
          for word in ["life-threatening", "critical condition", "immediate danger"]:
               explanation = explanation.replace(word, "clinically concerning")

     state["risk_level"] = risk
     state["triage_rationale"] = explanation.strip()
     state["escalation_required"] = escalation

     return state
