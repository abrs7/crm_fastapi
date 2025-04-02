from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogBase(BaseModel):
    entity: str
    entity_id: int
    action: str
    before_value: Optional[str] = None
    after_value: Optional[str] = None
    timestamp: datetime

class AuditLogResponse(AuditLogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Required for SQLAlchemy to Pydantic conversion
