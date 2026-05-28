from tests.conftest import client

import uuid

def create_client(payload):

    return client.post(
        "/clientes",
        json=payload
    )


def create_webhook(payload):

    return client.post(
        "/webhooks/pipefy/card-updated",
        json=payload
    )


def build_client_payload(
    patrimonio=300000
):

    unique_email = f"{uuid.uuid4()}@example.com"

    return {
        "cliente_nome": "Maria",
        "cliente_email": unique_email,
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": patrimonio
    }


def build_webhook_payload(
    email,
    event_id=None
):

    return {
        "event_id": event_id or str(uuid.uuid4()),
        "card_id": "card_001",
        "cliente_email": email,
        "timestamp": "2026-05-18T12:00:00Z"
    }