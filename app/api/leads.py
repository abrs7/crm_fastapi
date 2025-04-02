from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import leads as leads_crud
from app.database import SessionLocal
from app.schemas.leads import LeadCreate, Lead, LeadStatus
from app.models import UserAuth, UserRole
from app.auth import role_based, get_current_user
from typing import List


router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/leads/search", response_model=List[Lead])
async def search_leads_endpoint(query: str = Query(..., min_length=1), db: Session = Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    leads = leads_crud.search_leads(db, query)
    return leads


# Create a new lead
@router.post("/leads/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db),  current_user: UserAuth = Depends(get_current_user)):  # User ID is hardcoded for simplicity
    user_id = current_user.id
    return leads_crud.create_lead(db=db, lead=lead, user_id=user_id)

# Get all leads
@router.get("/leads/", response_model=list[Lead])
def get_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return leads_crud.get_leads(db=db, skip=skip, limit=limit)

# Get a specific lead by ID
@router.get("/leads/{lead_id}", response_model=Lead)
def get_lead_by_id(lead_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    db_lead = leads_crud.get_lead_by_id(db=db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

# Update lead status
@router.patch("/leads/{lead_id}/status", response_model=Lead)
async def update_lead_status(lead_id: int, lead_status: LeadStatus=LeadStatus.NEW,  db: Session = Depends(get_db), current_user: UserAuth = Depends(role_based(UserRole.manager))):
    db_lead = await leads_crud.update_lead_status(db=db, lead_id=lead_id, new_status=lead_status)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
