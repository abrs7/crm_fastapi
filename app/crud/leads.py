from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.model.leads import Lead
from app.models import UserAuth
from app.schemas.leads import LeadCreate
from app.utils.audit_log import log_audit_entry
import asyncio
from app.utils.notify_utils import notify_clients
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

def model_to_dict(model):
    """Convert SQLAlchemy model to a dictionary (excluding internal state)."""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}


# Create a new Lead
def create_lead(db: Session, lead: LeadCreate, user_id: int):
    db_lead = Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        status=lead.status,
        source=lead.source,
        created_by_id=user_id,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    # Log lead creation
    log_audit_entry(
        db=db,
        user_id=user_id,
        entity="lead",
        entity_id=db_lead.id,
        action="created",
        before=None,
        after=model_to_dict(db_lead),
    )
    return db_lead

# Get all leads
def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lead).offset(skip).limit(limit).all()

# Get a specific lead by ID
def get_lead_by_id(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()

# Update a lead's status
async def update_lead_status(db: Session, lead_id: int, new_status: str):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    before_lead = db_lead
    before_data = model_to_dict(db_lead)
    # before_data = db_lead.__dict__.copy()
    if not db_lead:
        return None 
    db_lead.status = new_status
    db.commit()
    db.refresh(db_lead)
    # Log status update
    log_audit_entry(
        db=db,
        user_id=1,
        entity="lead",
        entity_id=lead_id,
        action="updated",
        before=before_data,
        after=model_to_dict(db_lead),
    )    
    await notify_clients({
        "lead_id": lead_id,
        "before": before_data,
        "change": f"Lead model change from **{before_lead.status.value} --- to --- {new_status.value}",
        "after": model_to_dict(db_lead)
    })
    return db_lead


def search_leads(db: Session, query: str):
    return db.query(Lead).filter(
        or_(
            Lead.name.ilike(f"%{query}%"),
            Lead.email.ilike(f"%{query}%"),
            Lead.company.ilike(f"%{query}%")
        )
    ).all()