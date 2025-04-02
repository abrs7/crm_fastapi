from pydantic import BaseModel, conint, condecimal
from typing import List, Optional
from enum import Enum

# Quotation Status Enum
class QuotationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# Quotation Item Schema
class QuotationItemBase(BaseModel):
    description: str
    quantity: conint(ge=1)  # Ensure quantity is at least 1
    price: condecimal(ge=0)  # Ensure price is non-negative

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItem(QuotationItemBase):
    id: int

    class Config:
        orm_mode = True

# Quotation Schema
class QuotationBase(BaseModel):
    client_name: str
    status: QuotationStatus = QuotationStatus.DRAFT

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class QuotationUpdate(BaseModel):
    status: QuotationStatus

class Quotation(QuotationBase):
    id: int
    total_price: float
    items: List[QuotationItem]

    class Config:
        orm_mode = True
