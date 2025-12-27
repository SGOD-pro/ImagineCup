from fastapi import APIRouter, Depends, UploadFile, File

from app.core.container import get_clinical_service
from app.modules.clinical.clinical_service import ClinicalService
from app.modules.clinical.clinical_schemas import (
    OCRRequest,
    AnalysisRequest,
    AnalysisCaseRequest,
)

router = APIRouter(prefix="/clinical", tags=["Clinical"])


@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    service: ClinicalService = Depends(get_clinical_service),
):
    return await service.upload_files(files)


@router.post("/ocr")
async def run_ocr(
    req: OCRRequest,
    service: ClinicalService = Depends(get_clinical_service),
):
    return await service.extract_ocr(req.blob_ids)


@router.post("/analyze")
async def analyze_labs(
    req: AnalysisRequest,
    service: ClinicalService = Depends(get_clinical_service),
):
    return await service.analyze_labs(req)


@router.post("/analyze-case")
async def analyze_case(
    req: AnalysisCaseRequest,
    service: ClinicalService = Depends(get_clinical_service),
):
    return service.analyze_case(req)
