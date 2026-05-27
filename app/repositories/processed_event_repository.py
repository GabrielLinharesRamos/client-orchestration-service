from sqlalchemy.orm import Session
from app.models.processed_event import ProcessedEvent


class ProcessedEventRepository:

    @staticmethod
    def create(db: Session, event_data: dict):

        processed_event = ProcessedEvent(**event_data)

        db.add(processed_event)

        db.commit()

        db.refresh(processed_event)

        return processed_event

    @staticmethod
    def get_by_event_id(
        db: Session,
        event_id: str
    ):

        return (
            db.query(ProcessedEvent)
            .filter(ProcessedEvent.event_id == event_id)
            .first()
        )