from fastapi import FastAPI
from app.modules.clinical.clinical_controller import router as clinical_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="ClinAssist AI",
        version="1.0.0",
    )

    app.include_router(clinical_router)

    return app


app = create_app()

#run -> uvicorn app.main:app --reload
#prod-> uvicorn app.main:app --host 0.0.0.0 --port 8000