from app.core.logger import get_logger

logger = get_logger(__name__)

CREATE_CARD_MUTATION = """
mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_FIELD_MUTATION = """
mutation UpdateCardField($input: UpdateCardFieldInput!) {
  updateCardField(input: $input) {
    card {
      id
      title
    }
  }
}
"""


class PipefyService:

    @staticmethod
    def build_create_card_payload(client):

        return {
            "query": CREATE_CARD_MUTATION,
            "variables": {
                "input": {
                    "pipe_id": "123456",
                    "fields_attributes": [
                        {
                            "field_id": "cliente_nome",
                            "field_value": client.cliente_nome
                        },
                        {
                            "field_id": "cliente_email",
                            "field_value": client.cliente_email
                        },
                        {
                            "field_id": "tipo_solicitacao",
                            "field_value": client.tipo_solicitacao
                        },
                        {
                            "field_id": "valor_patrimonio",
                            "field_value": str(client.valor_patrimonio)
                        }
                    ]
                }
            }
        }

    @staticmethod
    def simulate_create_card(client):

        payload = PipefyService.build_create_card_payload(client)

        logger.info(
            "pipefy_create_card_simulated",
            extra={
                "client_email": client.cliente_email,
                "payload": payload
            }
        )

        return payload

    @staticmethod
    def build_update_card_payload(
        card_id,
        status,
        prioridade
    ):

        return {
            "query": UPDATE_CARD_FIELD_MUTATION,
            "variables": {
                "input": {
                    "card_id": card_id,

                    "fields_attributes": [
                        {
                            "field_id": "status",
                            "field_value": status
                        },
                        {
                            "field_id": "prioridade",
                            "field_value": prioridade
                        }
                    ]
                }
            }
        }

    @staticmethod
    def simulate_update_card(
        card_id,
        status,
        prioridade
    ):

        payload = PipefyService.build_update_card_payload(
            card_id=card_id,
            status=status,
            prioridade=prioridade
        )

        logger.info(
            "pipefy_update_card_simulated",
            extra={
                "card_id": card_id,
                "payload": payload
            }
        )

        return payload