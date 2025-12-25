from azure.storage.blob import BlobServiceClient,ContentSettings
import uuid

from app.config.blob_service import ACCOUNT_NAME,container_client

def upload_stream(file_stream, content_type: str) -> str:
     blob_name = f"{uuid.uuid4()}"
     blob_client = container_client.get_blob_client(blob_name)
     container_settings=ContentSettings(content_type=content_type)
     blob_client.upload_blob(
          file_stream,
          overwrite=True,
          content_settings=container_settings,
     )

     return blob_name