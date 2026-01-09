from fastapi import UploadFile, HTTPException,File
from typing import List
from app.domain.lab.normalizer import normalize_labs
from app.ai.state import ClinicalGraphState
from app.infrastructure.azure.ocr_client import OCRClient
from app.infrastructure.azure.blob_storage import BlobStorage
from app.ai.llm import NvidiaLLM
import json
import re
from typing import Dict, Any
def safe_json_load(raw: str) -> Dict[str, Any]:
    if not raw:
        raise ValueError("Empty LLM output")

    # Remove markdown code fences if present
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if fenced:
        raw = fenced.group(1)

    # Fallback: extract first JSON object
    brace_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if brace_match:
        raw = brace_match.group(0)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}\nRAW:\n{raw}")

class ClinicalService:
    def __init__(self, blob: BlobStorage, ocr: OCRClient, llm: NvidiaLLM, graph):
        self.blob = blob
        self.ocr = ocr
        self.llm = llm
        self.graph = graph

    async def upload_files(self, file: UploadFile= File(...)):
        blob_ids = []

        # for file in files:
        if file.content_type not in ("image/png","image/jpeg","application/pdf",):
            raise HTTPException(400, "Unsupported file type")

        blob_name = self.blob.upload_stream(
                file.file,
                file.content_type,
            )
        blob_ids.append(blob_name)

        return {"status": "uploaded", "blob_ids": blob_ids}

    async def extract_ocr(self, blob_ids: list[str]):
        documents = []

        for blob_id in blob_ids:
            blob = self.blob.generate_read_url(blob_id)

            if blob["content_type"] == "application/pdf":
                raw = self.ocr.extract_from_pdf(blob["url"])
            else:
                raw = self.ocr.extract_from_image(blob["url"])

            documents.append(raw)

        return {"ocr_texts": documents}


    async def analyze_labs(self, req):
        # 1. Merge OCR text
        merged_text = "\n".join(d["full_text"] for d in req.ocr_texts)

        # 2. LLM parses raw tests (NO MEDICAL LOGIC)
        raw = await self.llm.parse_labs(merged_text)
        parsed = safe_json_load(raw)
        normalized = normalize_labs(parsed["tests"], req.context)
        return {
            "labs": normalized,
            "symptoms": req.user_symptoms,
            "context": req.context
        }


    async def analyze_case(self, req):
        state: ClinicalGraphState = {
            "raw_symptoms_text": req.user_symptoms,
            "patient_age": req.context.age,
            "patient_gender": req.context.sex,
            "lab_results": req.labs,
            "clinical_signals": {},
            
            "structured_symptoms": None,
            "evidence": [],
            "lab_flags": {},
            "reasoning_summary": {},

            "hypotheses": [],
            "risk_level": None,
            "triage_rationale": None,
            "escalation_required": False,

            "safety_notes": None
        }
        result=await self.graph.ainvoke(state)
        return result
