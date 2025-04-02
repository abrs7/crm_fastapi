from fastapi import FastAPI, exception_handlers, Depends, HTTPException,status
from pydantic import BaseModel
from app.database import engine, SessionLocal
from app.auth import create_access_token, verify_password, get_current_user, hash_password, get_user_by_username, get_db, role_based
from app.models import UserRole, UserAuth, Base
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from app.api import leads, quotation  # Import lead api
from app.model.audit_logs import AuditLog
from app.crud.leads import model_to_dict
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from app.utils.notify_utils import active_connections

Base.metadata.create_all(bind=engine)
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
# print("Connected")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    





app = FastAPI()
app.include_router(leads.router, prefix="/api", tags=["Leads"])
app.include_router(quotation.router, prefix="/api", tags=["Quotations"])


@app.post("/register")
async def register(username: str, email:str, password: str,role:UserRole = UserRole.sales, db: Session = Depends(get_db)):
    print("Received Data:", username)
    existing_user = get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(password)
    new_user = UserAuth(username=username, email=email,role=role , hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "Welcome to CRM API!"}

@app.get("/audit_logs/{log_id}")
def get_audit_log(log_id: int, db: Session = Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    db_log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return model_to_dict(db_log)  # Convert SQLAlchemy object to dict before returning


@app.get("/audit_logs")
def get_audit_log(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),  current_user: UserAuth=Depends(get_current_user)):
    logs = db.query(AuditLog).offset(skip).limit(limit).all() 
    if not logs:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return [model_to_dict(log) for log in logs]


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)