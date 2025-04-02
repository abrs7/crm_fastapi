from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

# Enum for Quotation Status
class QuotationStatus(str, PyEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# Quotation Model
class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    status = Column(Enum(QuotationStatus), default=QuotationStatus.DRAFT, nullable=False)
    total_price = Column(Float, default=0.0)
    created_by_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("user_auth.id"), nullable=True)
    reason = Column(String, nullable=True)
    # Relationship to quotation items
    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete")
    created_by = relationship("UserAuth", foreign_keys=[created_by_id])
    approved_by = relationship("UserAuth", foreign_keys=[approved_by_id])

# Quotation Line Items
class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationship to quotation
    quotation = relationship("Quotation", back_populates="items")
