import uuid
import re
from typing import Dict, Any, List

# keep this SMALL and explicit
KNOWN_SYMPTOMS = [
    "cough", "fever", "weight loss", "night sweats",
    "shortness of breath", "chest pain", "vomiting",
    "diarrhoea", "abdominal pain", "jaundice",
    "fatigue", "anaemia", "hypotension", "tachycardia"
]

DURATION_REGEX = r"(more than|over|>|<)\s*\d+\s*(days|weeks|months|hours)"

def extract_symptoms(text: str) -> List[str]:
    text_l = text.lower()
    return [s for s in KNOWN_SYMPTOMS if s in text_l]

def extract_duration(text: str) -> str | None:
    m = re.search(DURATION_REGEX, text.lower())
    return m.group(0) if m else None

def build_embedding_text(
    disease: str | None,
    signal_type: str,
    symptoms: List[str],
    duration: str | None,
    action: str | None,
    statement: str
) -> str:
    return f"""
Disease: {disease}
Signal type: {signal_type}
Symptoms: {", ".join(symptoms)}
Duration: {duration}
Action: {action}
Guideline statement: {statement}
""".strip()

def normalize_record(raw: Dict[str, Any],disease: str,source: str) -> Dict[str, Any]:
    """
    raw = one extracted guideline sentence block
    """

    text = raw["text"]

    symptoms = extract_symptoms(text)
    duration = extract_duration(text)

    signal_type = (
        raw.get("category", ["early_warning"])[0]
        if isinstance(raw.get("category"), list)
        else raw.get("category", "early_warning")
    )


    action = None
    if signal_type == "escalation":
        action = "Immediate referral or urgent management"
    elif signal_type == "early_warning":
        action = "Further evaluation recommended"

    embedding_text = build_embedding_text(
        disease=disease,
        signal_type=signal_type,
        symptoms=symptoms,
        duration=duration,
        action=action,
        statement=text
    )

    return {
        "id": str(uuid.uuid4()),
        "embedding_text": embedding_text,
        "metadata": {
            "disease": disease,
            "signal_type": signal_type,
            "symptoms": symptoms,
            "duration": duration,
            "action": action,
            "source": source,
            "page": raw["metadata"].get("page")
        }
    }

import os
import json
JSON_SOURCES = [
    {
        "file": "DENGUE2.json",
        "disease": "dengue",
        "source": "WHO_DENGUE_GUIDELINES"
    },
    {
        "file": "GHANA.json",
        "disease": "general_clinical",
        "source": "GHANA_STG"
    },
    {
        "file": "HIVTB_Clinical_Guide_Primary_Care 2018_March2021_en.json",
        "disease": "hiv_tb",
        "source": "WHO_HIV_TB_PRIMARY_CARE"
    },
    {
        "file": "JBDS_02_DKA_Guideline_with_QR_code_March_2023.json",
        "disease": "dka",
        "source": "JBDS_DKA_2023"
    },
    {
        "file": "KDIGO-2024-CKD-Guideline.json",
        "disease": "ckd",
        "source": "KDIGO_CKD_2024"
    },
    {
        "file": "NONCOMMUNICABLE (PEN).json",
        "disease": "ncd",
        "source": "WHO_PEN"
    },
    {
        "file": "Operational-Manual-for-Tuberculosis_compressed.json",
        "disease": "tuberculosis",
        "source": "WHO_TB_MANUAL"
    },
    {
        "file": "pneumonia-diagnosis-and-management-pdf-66144010347205.json",
        "disease": "pneumonia",
        "source": "WHO_PNEUMONIA"
    },
    {
        "file": "Prevention and treatment of.json",
        "disease": "general_emergency",
        "source": "WHO_EMERGENCY_CARE"
    },
    {
        "file": "Surviving-Sepsis-Campaign_International-Guidelines-for-Management-of-Sepsis-and-Septic-Shock-2021.json",
        "disease": "sepsis",
        "source": "SSC_SEPSIS_2021"
    },
    {
        "file": "WHO malaria guidelines - August 2025.json",
        "disease": "malaria",
        "source": "WHO_MALARIA_2025"
    }
]
os.makedirs("cleaned_data", exist_ok=True)

if __name__ =="__main__":
     # json_files=[]
     # for filename in os.listdir("extracted_data"):
     #      path = os.path.join("extracted_data", filename)
          
     #      if os.path.isfile(path):
     #           json_files.append(path)
     # print(json_files)



     for json_file in JSON_SOURCES:
          normalized_docs = []
          raw_json = []
          with open(f"extracted_data"+"/"+json_file["file"], "r", encoding="utf-8") as f:
               raw_json = json.load(f)
          
          for record in raw_json:
               cleaned = normalize_record(
                    record,
                    disease=json_file["disease"],
                    source=json_file["source"]
               )
               normalized_docs.append(cleaned)

     
          with open(f"cleaned_data"+"/"+json_file["file"], "w", encoding="utf-8") as f:
                json.dump(normalized_docs, f, indent=2, ensure_ascii=False)