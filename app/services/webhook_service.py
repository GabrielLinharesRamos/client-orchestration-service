from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.repositories.processed_event_repository import ProcessedEventRepository
from app.schemas.webhooks import PipefyWebhookPayload

class WebhookService:

    @staticmethod
    def calculate_priority(valor_patrimonio: float):

        if valor_patrimonio >= 200000:
            return "prioridade_alta"

        return "prioridade_normal"

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

        client = ClientRepository.get_by_email(
            db,
            payload.cliente_email
        )

        if not client:
            raise ValueError("Cliente não encontrado")

        client.prioridade = WebhookService.calculate_priority(
            client.valor_patrimonio
        )

        client.status = "Processado"

        ClientRepository.update(db, client)

        event = ProcessedEventRepository.create(
            db=db,
            event_data=event_data
        )

        return client