import uuid

from tests.conftest import client


def create_client_and_assert(
    cliente_nome,
    cliente_email,
    tipo_solicitacao,
    valor_patrimonio,
    response
):

    payload = {
        "cliente_nome": cliente_nome,
        "cliente_email": cliente_email,
        "tipo_solicitacao": tipo_solicitacao,
        "valor_patrimonio": valor_patrimonio
    }

    response = client.post(
        "/clientes",
        json=payload
    )

    assert response.status_code == response

    data = response.json()

    assert data["cliente_nome"] == cliente_nome

    assert data["cliente_email"] == cliente_email

    assert data["status"] == "Aguardando Análise"

    return data


def test_create_client_success():

    unique_email = f"{uuid.uuid4()}@example.com"

    create_client_and_assert(
        "João Silva",
        unique_email,
        "Atualização cadastral",
        250000,
        201
    )