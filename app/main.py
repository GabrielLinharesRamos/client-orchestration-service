from fastapi import FastAPI

from app.core.database import engine
from app.models.client import Client
from app.core.database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}