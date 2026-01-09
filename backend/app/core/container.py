from functools import lru_cache

from app.infrastructure.azure.ocr_client import OCRClient
from app.infrastructure.azure.blob_storage import BlobStorage
from app.ai.llm import NvidiaLLM
from app.ai.graph import build_clinical_graph
from app.modules.clinical.clinical_service import ClinicalService


@lru_cache()
def get_clinical_service() -> ClinicalService:
    return ClinicalService(
        blob=BlobStorage(),
        ocr=OCRClient(),
        llm=NvidiaLLM(),
        graph=build_clinical_graph(),
    )
