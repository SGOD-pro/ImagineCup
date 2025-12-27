from app.ai.state import ClinicalGraphState
# from langchain_nvidia import ChatNVIDIA
from app.ai.llm import NvidiaLLM
import json
'''Symptom Structuring Agent (SSA)'''

async def ssa_node(state: ClinicalGraphState) -> ClinicalGraphState:
     prompt = f"""
You are a clinical symptom structuring agent.

Input:
Age: {state['patient_age']}
Gender: {state['patient_gender']}
Symptoms: {state['raw_symptoms_text']}

Task:
Extract and return a JSON object with:
- chief_complaints (list of strings)
- duration (string or null)
- severity (string or null)
- red_flags (list of strings)

Rules:
- Do NOT mention diseases
- Do NOT provide diagnosis
- Output JSON only, no extra text.
"""

     llm = NvidiaLLM(model_name="nvidia/nemotron-3-nano-30b-a3b", temp=0.2)
     response = llm.model.invoke(prompt)
     try:
          structured = json.loads(str(response.content))
          required_keys = {"chief_complaints", "duration", "severity", "red_flags"}
          if not required_keys.issubset(structured.keys()):
               raise ValueError("SSA output schema invalid")
     except Exception as e:
          raise ValueError(f"SSA output invalid: {e}")
     return {
          **state,
          "structured_symptoms": structured
     }



