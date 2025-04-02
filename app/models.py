from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, Enum as SQLEnum,  DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum
from app.database import Base
from datetime import datetime

# Base.metadata.create_all(bind=engine)
# Base = declarative_base()
class UserRole(Enum):
    sales = "sales"
    admin = "admin"
    manager = "manager"
    all_roles = "all_roles"


class UserAuth(Base):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole, name="user_role"), nullable=False, default=UserRole.sales.value)
    is_active = Column(Boolean, default=True)
    # Relationship to UserProfile
    profile = relationship("UserProfile", back_populates="auth", uselist=False)
    # Relationship to Leads
    leads = relationship("Lead", back_populates="created_by")
    audit_logs = relationship("AuditLog", back_populates="user")



class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(Integer, ForeignKey("user_auth.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    address = Column(String, nullable=True)

    # Relationship back to UserAuth
    auth = relationship("UserAuth", back_populates="profile")    

