from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.client import (
    PipefyWebhookPayload
)

from app.services.client_service import (
    ClientService
)

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]
)


@router.post(
    "",
    response_model=ClientResponse,
    status_code=201
)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db)
):

    try:

        client = ClientService.create_client(
            db=db,
            payload=payload
        )

        return client

    except ValueError as error:

        raise HTTPException(
            status_code=409,
            detail=str(error)
        )