from tests.helpers import (
    create_client,
    create_webhook,
    build_webhook_payload,
    build_client_payload
)

import uuid

def test_webhook_priority_high():

    client_payload = build_client_payload(
        patrimonio=300000
    )

    create_client(client_payload)

    webhook_payload = build_webhook_payload(
        email=client_payload["cliente_email"]
    )

    response = create_webhook(webhook_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["client"]["status"] == "Processado"

    assert data["client"]["prioridade"] == "prioridade_alta"


def test_webhook_priority_low():

    client_payload = build_client_payload(
        patrimonio=100000
    )

    create_client(client_payload)

    webhook_payload = build_webhook_payload(
        email=client_payload["cliente_email"]
    )

    response = create_webhook(webhook_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["client"]["status"] == "Processado"

    assert data["client"]["prioridade"] == "prioridade_normal"


def test_duplicate_event_id():

    client_payload = build_client_payload()

    create_client(client_payload)

    fixed_event_id = str(uuid.uuid4())

    webhook_payload = build_webhook_payload(
        email=client_payload["cliente_email"],
        event_id=fixed_event_id
    )

    first_response = create_webhook(webhook_payload)

    second_response = create_webhook(webhook_payload)

    assert first_response.status_code == 200

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["detail"] == "O evento já foi processado"