from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    nome: str
    email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float


class ClientResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    status: str