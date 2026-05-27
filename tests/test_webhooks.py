from tests.conftest import client
import uuid

def test_webhook_priority_high():

    unique_email = f"{uuid.uuid4()}@example.com"

    unique_event_id = f"{uuid.uuid4()}"

    client_payload = {
        "cliente_nome": "Maria",
        "cliente_email": unique_email,
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 300000
    }

    client.post(
        "/clientes",
        json=client_payload
    )

    webhook_payload = {
        "event_id": unique_event_id,
        "card_id": "card_001",
        "cliente_email": unique_email,
        "timestamp": "2026-05-18T12:00:00Z"
    }

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json=webhook_payload
    )

    assert response.status_code == 200