from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate
from app.services.pipefy_services import PipefyService

class ClientService:

    @staticmethod
    def create_client(
        db: Session,
        payload: ClientCreate
    ):

        existing_client = ClientRepository.get_by_email(
            db=db,
            cliente_email=payload.cliente_email
        )

        if existing_client:

            raise ValueError(
                "Já existe um cliente com este email"
            )

        client_data = {
            "cliente_nome": payload.cliente_nome,
            "cliente_email": payload.cliente_email,
            "tipo_solicitacao": payload.tipo_solicitacao,
            "valor_patrimonio": payload.valor_patrimonio,
            "status": "Aguardando Análise",
            "prioridade": None
        }

        client = ClientRepository.create(
            db=db,
            client_data=client_data
        )

        PipefyService.simulate_create_card(client)

        return client