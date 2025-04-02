from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

# Enum for LeadStatus & LeadSource
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

# Pydantic Base model for creating a Lead
class LeadBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource

# Pydantic model for creating a lead (used in POST)
class LeadCreate(LeadBase):
    pass

# Pydantic model for reading a lead (used in GET)
class Lead(LeadBase):
    id: int
    created_by_id: int  # The ID of the user who created the lead

    class Config:
        orm_mode = True
