from fastapi import FastAPI
from uvicorn import run
from app.api.routes import router

app = FastAPI()
app.include_router(router=router)

if __name__ =="__main":
    run(app, reload=True,port=8000,host="0.0.0.0")
