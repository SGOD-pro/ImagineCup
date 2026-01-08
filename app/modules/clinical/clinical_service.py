from fastapi import UploadFile, HTTPException
from typing import List
from app.domain.lab.normalizer import normalize_labs
from app.ai.state import ClinicalGraphState
from app.infrastructure.azure.ocr_client import OCRClient
from app.infrastructure.azure.blob_storage import BlobStorage
from app.ai.llm import NvidiaLLM
class ClinicalService:
    def __init__(self, blob: BlobStorage, ocr: OCRClient, llm: NvidiaLLM, graph):
        self.blob = blob
        self.ocr = ocr
        self.llm = llm
        self.graph = graph

    async def upload_files(self, files: List[UploadFile]):
        blob_ids = []

        for file in files:
            if file.content_type not in (
                "image/png",
                "image/jpeg",
                "application/pdf",
            ):
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
        print(raw)
        parsed = __import__("json").loads(raw)
        normalized = normalize_labs(parsed["tests"], req.context)
        return {
            "labs": normalized,
            "symptoms": req.user_symptoms,
            "context": req.context
        }


    async def analyze_case(self, req):
        state: ClinicalGraphState = {
            "raw_symptoms_text": req.symptoms,
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
