from fastapi import FastAPI
from app.api.routes.clients import router as client_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(client_router)


@app.get("/health")
def health():
    return {"status": "ok"}