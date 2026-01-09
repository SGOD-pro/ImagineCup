from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from app.core.blob_service import container_client, ACCOUNT_NAME, ACCOUNT_KEY
from app.core import settings
import uuid
from azure.storage.blob import ContentSettings

class BlobStorage:
    
    def generate_read_url(self, blob_name: str) -> dict:
        blob_client = container_client.get_blob_client(blob_name)
        props = blob_client.get_blob_properties()
        
        if ACCOUNT_NAME is None or ACCOUNT_KEY is None:
            raise RuntimeError("ACCOUNT_NAME or ACCOUNT_KEY is not set")
        
        sas = generate_blob_sas(
            account_name=ACCOUNT_NAME,
            container_name=settings.CONTAINER_NAME,
            blob_name=blob_name,
            account_key=ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=10),
        )

        return {
            "url": f"{container_client.url}/{blob_name}?{sas}",
            "content_type": props.content_settings.content_type,
        }
        
    def upload_stream(self,file_stream, content_type: str) -> str:
        blob_name = f"{uuid.uuid4()}"
        blob_client = container_client.get_blob_client(blob_name)
        container_settings=ContentSettings(content_type=content_type)
        blob_client.upload_blob(
            file_stream,
            overwrite=True,
            content_settings=container_settings,
        )

        return blob_name
