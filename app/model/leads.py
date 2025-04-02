from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.database import Base

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    LOST = "lost"

class LeadSource(str, Enum):
    WEBSITE = "website"
    LINKEDIN = "linkedin"
    SOCIAL_MEDIA = "social_media"
    REFERRAL = "referral"
    OTHER = "other"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    company = Column(String, nullable=True)
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    source = Column(SQLEnum(LeadSource), nullable=False)

    # Relationship (assuming a user can create multiple leads)
    created_by_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)
    created_by = relationship("UserAuth", back_populates="leads")