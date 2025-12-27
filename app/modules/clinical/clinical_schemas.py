from pydantic import BaseModel
from typing import Dict, Any, List

class OCRRequest(BaseModel):
    blob_ids: list[str]

class AnalysisRequest(BaseModel):
    ocr_texts: List[Dict[str, Any]]
    user_symptoms: str
    context: Dict[str, Any]

class Context(BaseModel):
    age: int
    sex: str

class AnalysisCaseRequest(BaseModel):
    labs: List[Dict[str, Any]]
    symptoms: str
    context: Context