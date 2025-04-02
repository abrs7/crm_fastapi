from sqlalchemy.orm import Session
import json
from app.model.audit_logs import AuditLog

def log_audit_entry(
    db: Session,
    user_id: int,
    entity: str,
    entity_id: int,
    action: str,
    before: dict = None,
    after: dict = None,
):
    audit_entry = AuditLog(
        user_id=user_id,
        entity=entity,
        entity_id=entity_id,
        action=action,
        before_value=json.dumps(before) if before else None,
        after_value=json.dumps(after) if after else None,
    )
    db.add(audit_entry)
    db.commit()
