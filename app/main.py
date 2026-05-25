from fastapi import FastAPI
from app.api.routes.clients import router as client_router

app = FastAPI()

app.include_router(client_router)


@app.get("/health")
def health():
    return {"status": "ok"}