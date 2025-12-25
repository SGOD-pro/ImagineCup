from fastapi import APIRouter, UploadFile, File, HTTPException
from app.azure.upload import upload_stream
from app.azure.blob_client import generate_sas
from app.azure.OCR import blob_image_result,blob_doc_result
router = APIRouter()


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    #TODO: Do text extraction if it was a PDF
    blob_name = upload_stream(
        file.file,  # THIS IS A STREAM
        file.content_type
    )
    print(blob_name)
    return {
        "status": "uploaded",
        "blob_name": blob_name
    }

@router.get("/analyze/{blob_name}")
async def get_data(blob_name: str):
    blob=generate_sas(blob_name)
    if blob is None:
        raise HTTPException(status_code=404, detail="Blob not found")
    if blob.content_type == "application/pdf":
        result=blob_doc_result(blob.url)
    else:
        result=blob_image_result(blob.url)
    return {
        "status": "text",
        "result": result
    }