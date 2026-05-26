from sqlalchemy.orm import Session
from app.models.client import Client


class ClientRepository:

    @staticmethod
    def create(db: Session, client_data: dict):

        client = Client(**client_data)

        db.add(client)

        db.commit()

        db.refresh(client)

        return client

    @staticmethod
    def get_by_email(
        db: Session,
        cliente_email: str
    ):

        return (
            db.query(Client)
            .filter(Client.cliente_email == cliente_email)
            .first()
        )