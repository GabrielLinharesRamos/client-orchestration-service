from pydantic import BaseModel, EmailStr, field_validator


class ClientCreate(BaseModel):
    nome: str
    email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

    @field_validator("nome", "tipo_solicitacao")
    @classmethod
    def validate_not_empty(cls, value: str):

        if not value.strip():
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("valor_patrimonio")
    @classmethod
    def validate_patrimonio(cls, value: float):

        if value <= 0:
            raise ValueError("valor_patrimonio must be positive")
        
        return value

class ClientResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    status: str