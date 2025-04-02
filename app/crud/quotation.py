from sqlalchemy.orm import Session
from app.model.quotation import Quotation, QuotationItem, QuotationStatus
from app.schemas.quotation import QuotationCreate, QuotationUpdate
from app.utils.audit_log import log_audit_entry
from app.utils.notify_utils import notify_clients

def model_to_dict(model):
    """Convert SQLAlchemy model to a dictionary (excluding internal state)."""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}


# Create a Quotation
def create_quotation(db: Session, quotation: QuotationCreate, user_id: int):
    db_quotation = Quotation(
        client_name=quotation.client_name,
        created_by_id=user_id,
        status=quotation.status
    )
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)

    # Add line items
    total_price = 0
    for item in quotation.items:
        db_item = QuotationItem(
            quotation_id=db_quotation.id,
            description=item.description,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
        total_price += item.quantity * item.price

    db_quotation.total_price = total_price
    db.commit()
    log_audit_entry(
        db=db,
        user_id=user_id,
        entity="quotation",
        entity_id=db_quotation.id,
        action="created",
        before=None,
        after=model_to_dict(db_quotation),
    )
    return db_quotation

# Get all Quotations
def get_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quotation).offset(skip).limit(limit).all()

# Get a specific Quotation by ID
def get_quotation_by_id(db: Session, quotation_id: int):
    return db.query(Quotation).filter(Quotation.id == quotation_id).first()

# Update Quotation Status
async def update_quotation_status(db: Session, quotation_id: int, update_data: QuotationStatus, user_id: str):
    db_quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    before_quotation = db_quotation
    before = model_to_dict(db_quotation)
    if db_quotation:
        db_quotation.status = update_data
        db.commit()
        db.refresh(db_quotation)

    log_audit_entry(
        db=db,
        user_id=user_id,
        entity="quotation",
        entity_id=db_quotation.id,
        action="created",
        before=before,
        after=model_to_dict(db_quotation),
    )  
    await notify_clients({
        "quotation_id": quotation_id,
        "before": before,
        "change": f"Lead model change from **{before_quotation.status.value} --- to --- {update_data.value}",
        "after": model_to_dict(db_quotation)
    })  
    return db_quotation


def approve_quotation(db: Session, quote_id: int, manager_id: str, reason: str):
    db_quote = db.query(Quotation).filter(Quotation.id == quote_id).first()
    if not db_quote:
        return None  # Quote not found
    
    db_quote.status = QuotationStatus.APPROVED
    db_quote.reason = reason
    db_quote.approved_by_id = manager_id
    db.commit()
    db.refresh(db_quote)
    return db_quote

def reject_quotation(db: Session, quote_id: int, manager_id: str, reason: str):
    db_quote = db.query(Quotation).filter(Quotation.id == quote_id).first()
    if not db_quote:
        return None  # Quote not found
    
    db_quote.status = QuotationStatus.REJECTED
    db_quote.reason = reason
    db_quote.approved_by_id = manager_id
    db.commit()
    db.refresh(db_quote)
    return db_quote