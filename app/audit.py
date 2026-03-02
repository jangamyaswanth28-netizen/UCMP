
from .models import AuditLog

def log_audit(db, event_id, action, actor):
    audit = AuditLog(
        event_id=event_id,
        action_type=action,
        performed_by=actor
    )
    db.add(audit)
    db.commit()
