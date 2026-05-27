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
                "client_email": client.client_email,
                "payload": payload
            }
        )

        return payload

