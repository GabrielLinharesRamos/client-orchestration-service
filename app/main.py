from app.core.database import Base, engine

from app.models.client import Client
from app.models.processed_event import ProcessedEvent

from fastapi import FastAPI

from app.api.routes.clients import router as event_router
from app.api.routes.webhooks import router as client_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(client_router)
app.include_router(event_router)


@app.get("/health")
def health():
    return {"status": "ok"}