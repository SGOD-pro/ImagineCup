from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient,ContentSettings
from app.config.blob_service import ACCOUNT_KEY,ACCOUNT_NAME,container_client
from app.config import settings
from pydantic import BaseModel

class Blob(BaseModel):
    url: str
    content_type:str

def generate_sas(blob_name: str) -> Blob:
    if ACCOUNT_NAME is None or ACCOUNT_KEY is None:
        raise RuntimeError("ACCOUNT_NAME or ACCOUNT_KEY is not set")
    
    blob_client = container_client.get_blob_client(blob_name)
    props = blob_client.get_blob_properties()

    sas = generate_blob_sas(
        account_name=ACCOUNT_NAME,
        container_name=settings.CONTAINER_NAME,
        blob_name=blob_name,
        account_key=ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=10),
        
    )

    return Blob(
            url=f"{container_client.url}/{blob_name}?{sas}",
            content_type=f"{props.content_settings.content_type}"
        )
