from fastapi import APIRouter, UploadFile, File, HTTPException
from app.azure.upload import upload_stream
from app.azure.blob_client import generate_sas
from app.azure.OCR import blob_image_result,blob_doc_result
from pydantic import BaseModel
from typing import List
from app.helper.cleanup import normalize_labs
from typing import Dict, Any, List
from app.ai.promts import labs
from langchain.messages import HumanMessage
import json
from fastapi.concurrency import run_in_threadpool
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from app.config import settings
from app.ai.graph import graph
from app.ai.state import ClinicalGraphState

router = APIRouter()



@router.post("/upload")
async def upload_file(files: list[UploadFile] = File(...)):
    blob_ids = []

    for file in files:
        if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
            raise HTTPException(400, "Unsupported file type")

        blob_name = upload_stream(file.file, file.content_type)
        blob_ids.append(blob_name)

    return {
        "status": "uploaded",
        "blob_ids": blob_ids
    }

class OCRRequest(BaseModel):
    blob_ids: list[str]

@router.post("/ocr")
async def get_data(req: OCRRequest):
    documents = []

    for blob_id in req.blob_ids:
        blob = generate_sas(blob_id)
        if blob.content_type == "application/pdf":
            raw = blob_doc_result(blob.url)
        else:
            raw = blob_image_result(blob.url)

        # canonical = normalize_ocr(raw) 
        documents.append(raw)
    #BUG: IF THE RAW FROM 2 DOCS/IMAGES ARE THE SAME, IGNORE ONE.
    return {
        "ocr_texts": documents
    }



class AnalysisRequest(BaseModel):
    ocr_texts: List[Dict[str, Any]]
    user_symptoms: str
    context: Dict[str, Any]


@router.post("/analyze")
async def analyze(data: AnalysisRequest):
    """
    Expected input:
    {
        "ocr_texts": [
            {
                "source": "image",
                "full_text": "..."
            },
            {
                "source": "pdf",
                "full_text": "..."
            }
        ],
        "user_symptoms": "fatigue, fever",
        "context": {
            "age": 21,
            "sex": "male"
        }
    }
    """

    # 1. Merge OCR texts
    merged_text = "\n".join(doc["full_text"] for doc in data.ocr_texts)
  
    # 2. Parse labs (rule → LLM fallback)
    model= ChatNVIDIA(
        model_name="nvidia/nvidia-nemotron-nano-9b-v2",
        temp=.1,
        api_key=settings.NIM_API,
        max_tokens=4096
    )
    prompt = labs + merged_text
    response = await run_in_threadpool(
        model.invoke,
        [HumanMessage(prompt)]
    )
    # response = model.invoke([HumanMessage("Hii januuu")])
    # print(response.content)
    raw_output = str(response.content)

    # 3. Normalize + validate labs
    parsed = json.loads(raw_output)
    
    normalized_labs = normalize_labs(parsed["tests"])
    # return {"status":parsed}

    # 4. Build medical state
    medical_state = {
        "labs": normalized_labs,
        "symptoms": data.user_symptoms,
        "context": data.context
    }

    # 5. Pass ONLY THIS to agentic graph
    #result = run_agent_graph(medical_state)

    return medical_state

class Context(BaseModel):
    age: int
    sex: str

class AnalysisCaseRequest(BaseModel):
    labs: List[Dict[str, Any]]
    symptoms: str
    context: Context


@router.post("/analyze-csae")
async def analyze_case(data:AnalysisCaseRequest):
    initial_state: ClinicalGraphState = {
    "raw_symptoms_text": data.symptoms,
    "patient_age": data.context.age,
    "patient_gender": data.context.sex,
    "lab_results": data.labs,

    # initialize graph-owned fields
    "structured_symptoms": None,
    "evidence": [],
    "hypotheses": [],
    "risk_level": None,
    "escalation_required": False,
    "triage_rationale": None
}

    result=graph.invoke(input=initial_state)

    return result