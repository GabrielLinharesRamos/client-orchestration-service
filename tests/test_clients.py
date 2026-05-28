from tests.helpers import (
    create_client,
    build_client_payload
)


def test_create_new_client():

    payload = build_client_payload()

    response = create_client(payload)

    assert response.status_code == 201

    data = response.json()

    assert data["cliente_nome"] == payload["cliente_nome"]

    assert data["cliente_email"] == payload["cliente_email"]

    assert data["status"] == "Aguardando Análise"


def test_create_already_existing_client():

    payload = build_client_payload()

    first_response = create_client(payload)

    second_response = create_client(payload)

    assert first_response.status_code == 201

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == "Já existe um cliente com este email"