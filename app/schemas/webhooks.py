from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class PipefyWebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime