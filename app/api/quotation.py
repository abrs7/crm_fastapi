from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import quotation as crud
from app.database import SessionLocal
from app.schemas.quotation import QuotationCreate, QuotationUpdate, Quotation, QuotationStatus
from app.models import UserAuth, UserRole
from app.auth import role_based, get_current_user
router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new Quotation
@router.post("/quotations/", response_model=Quotation)
def create_quotation(quotation: QuotationCreate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    user_id = current_user.id
    return crud.create_quotation(db=db, quotation=quotation, user_id=user_id)

# Get all Quotations
@router.get("/quotations/", response_model=list[Quotation])
def get_quotations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),  current_user: UserAuth = Depends(role_based(UserRole.manager))):
    return crud.get_quotations(db=db, skip=skip, limit=limit)

# Get a specific Quotation by ID
@router.get("/quotations/{quotation_id}", response_model=Quotation)
def get_quotation_by_id(quotation_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(role_based(UserRole.manager))):
    db_quotation = crud.get_quotation_by_id(db=db, quotation_id=quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation

# Update Quotation Status
@router.patch("/quotations/{quotation_id}/status", response_model=Quotation)
async def update_quotation_status(quotation_id: int, new_status: QuotationStatus=QuotationStatus.DRAFT, db: Session = Depends(get_db),current_user: UserAuth = Depends(role_based(UserRole.manager))):
    user_id = current_user.id
    db_quotation = await crud.update_quotation_status(db=db, quotation_id=quotation_id, update_data=new_status, user_id=user_id)
    
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation


@router.post("/quotations/{quote_id}/approve")
def approve_quote(quote_id: int, reason:str, db: Session = Depends(get_db), current_user: UserAuth = Depends(role_based(UserRole.manager))):
    if current_user.role != UserRole.manager:
        raise HTTPException(status_code=403, detail="Only managers can approve quotes")
    
    approved_quote = crud.approve_quotation(db, quote_id, current_user.id, reason)
    if not approved_quote:
        raise HTTPException(status_code=404, detail="Quotation not found")
    
    return {"message": "Quotation approved successfully", "quotation": approved_quote}

@router.post("/quotations/{quote_id}/reject")
def reject_quote(quote_id: int, reason: str, db: Session = Depends(get_db), current_user: UserAuth = Depends(role_based(UserRole.manager))):
    if current_user.role != UserRole.manager:
        raise HTTPException(status_code=403, detail="Only managers can reject quotes")

    rejected_quote = crud.reject_quotation(db, quote_id, current_user.id, reason)
    if not rejected_quote:
        raise HTTPException(status_code=404, detail="Quotation not found")
    
    return {"message": "Quotation rejected successfully", "quotation": rejected_quote}