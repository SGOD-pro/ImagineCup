from azure.storage.blob import BlobServiceClient,ContentSettings
from app.core import settings

blob_service = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)


container_client = blob_service.get_container_client(settings.CONTAINER_NAME)

ACCOUNT_NAME = blob_service.account_name

ACCOUNT_KEY=blob_service.credential.account_key

assert ACCOUNT_KEY is not None  # runtime + type safety
assert ACCOUNT_NAME is not None  # runtime + type safety