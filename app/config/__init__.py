from pydantic_settings import BaseSettings

class Settings(BaseSettings):
     VISION_KEY: str = ""
     VISION_ENDPOINT: str=""
     NIM_API: str=""
     QDRANT_URL: str=""
     QDRANT_KEY: str=""
     AZURE_STORAGE_CONNECTION_STRING: str = "HS256"
     CONTAINER_NAME: str=""
     DOCUMENT_INTELLIGENCE_ENDPOINT:str=""
     DOCUMENT_INTELLIGENCE_KEY:str=""
     class Config:
          env_file = ".env"

settings = Settings() # type: ignore
