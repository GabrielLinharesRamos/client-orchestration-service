from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate


class ClientService:

    @staticmethod
    def create_client(
        db: Session,
        payload: ClientCreate
    ):

        existing_client = ClientRepository.get_by_email(
            db=db,
            email=payload.email
        )

        if existing_client:

            raise ValueError(
                "Já existe um cliente com este email"
            )

        client_data = {
            "nome": payload.nome,
            "email": payload.email,
            "tipo_solicitacao": payload.tipo_solicitacao,
            "valor_patrimonio": payload.valor_patrimonio,
            "status": "Aguardando Análise",
            "prioridade": None
        }

        client = ClientRepository.create(
            db=db,
            client_data=client_data
        )

        return client