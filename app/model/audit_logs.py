from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum,  DateTime, Text
from sqlalchemy.orm import relationship
from enum import Enum
from app.database import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)
    entity = Column(String, nullable=False)  # Example: "lead", "quotation"
    entity_id = Column(Integer, nullable=False)  # ID of the changed object
    action = Column(String, nullable=False)  # Example: "created", "updated", "deleted"
    before_value = Column(Text, nullable=True)  # JSON-like string for old data
    after_value = Column(Text, nullable=True)  # JSON-like string for new data
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAuth", back_populates="audit_logs")
