from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    tipo_solicitacao = Column(String, nullable=False)

    valor_patrimonio = Column(Float, nullable=False)

    status = Column(String, nullable=False)

    prioridade = Column(String, nullable=True)