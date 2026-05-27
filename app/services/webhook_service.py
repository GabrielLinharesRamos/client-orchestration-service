from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.repositories.processed_event_repository import ProcessedEventRepository
from app.schemas.webhooks import PipefyWebhookPayload

class WebhookService:

    @staticmethod
    def process_webhook(
        db: Session,
        payload: PipefyWebhookPayload
    ):

        existing_event = ProcessedEventRepository.get_by_event_id(
            db=db,
            event_id=payload.event_id
        )

        if existing_event:

            raise ValueError(
                "O evento já foi processado"
            )

        event_data = {
            "event_id": payload.event_id,
            "client_email": payload.cliente_email,
            "processed_at": payload.timestamp
        }

        event = ProcessedEventRepository.create(
            db=db,
            event_data=event_data
        )

        client = ClientRepository.get_by_email(
            db,
            payload.cliente_email
        )

        if client.valor_patrimonio >= 200000:
            prioridade = "prioridade_alta"
        else:
            prioridade = "prioridade_normal"

        client.status = "Processado"

        client.prioridade = prioridade

        ClientRepository.update(db, client)

        return event