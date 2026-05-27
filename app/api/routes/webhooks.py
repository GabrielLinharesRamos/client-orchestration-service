from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.webhooks import PipefyWebhookPayload

from app.services.webhook_service import WebhookService


router = APIRouter(
    prefix="/webhooks/pipefy",
    tags=["webhooks"]
)


@router.post(
    "/card-updated",
    status_code=200
)
def process_pipefy_webhook(
    payload: PipefyWebhookPayload,
    db: Session = Depends(get_db)
):

    try:

        event = WebhookService.process_webhook(
            db=db,
            payload=payload
        )

        return {
            "message": "Webhook processado com sucesso",
            "client": client
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )