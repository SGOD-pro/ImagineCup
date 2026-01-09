from fastapi import FastAPI
from app.modules.clinical.clinical_controller import router as clinical_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="ClinAssist AI",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080","http://10.5.145.113:8080","http://10.5.146.66:8080"],
        allow_methods=["*"],
        allow_credentials=True,
    )
    app.include_router(clinical_router)
    app.get("/health", tags=["Health"])(lambda: {"message": "Healthy..!"})
    return app


app = create_app()

#run -> uvicorn app.main:app --reload
#prod-> uvicorn app.main:app --host 0.0.0.0 --port 8000