
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .models import ConsentEvent, ConsentCurrent

def upsert_event(db: Session, event: ConsentEvent):
    existing = db.query(ConsentEvent).filter(
        and_(
            ConsentEvent.user_id == event.user_id,
            ConsentEvent.consent_type_id == event.consent_type_id,
            ConsentEvent.sequence_number == event.sequence_number
        )
    ).first()

    if existing:
        return existing

    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def update_current(db: Session, event: ConsentEvent):
    current = db.query(ConsentCurrent).filter(
        and_(
            ConsentCurrent.user_id == event.user_id,
            ConsentCurrent.consent_type_id == event.consent_type_id
        )
    ).with_for_update().first()

    if not current:
        current = ConsentCurrent(
            user_id=event.user_id,
            consent_type_id=event.consent_type_id,
            status=event.status,
            latest_sequence_number=event.sequence_number
        )
        db.add(current)
    else:
        if event.sequence_number > current.latest_sequence_number:
            current.status = event.status
            current.latest_sequence_number = event.sequence_number

    db.commit()
    return current
