# app/schemas/userSchema.py

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


# -----------------------------------
# User Roles
# -----------------------------------
class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    EXECUTIVE = "executive"
    PATIENT = "patient"
    NURSE = "nurse"


# -----------------------------------
# Base User Schema
# -----------------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    dob: Optional[str] = None
    is_active: bool = True
    profile_pic: Optional[str] = None


# -----------------------------------
# Create User Schema
# Used for Create User API
# -----------------------------------
class UserCreate(UserBase):
    password: str


# -----------------------------------
# Login Schema
# Used for Login API
# Only email + password required
# -----------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------------
# Update User Schema
# -----------------------------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


# -----------------------------------
# User Response Schema
# -----------------------------------
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------------
# Login Response Schema
# -----------------------------------
class UserLoginResponse(BaseModel):
    success: bool
    message: str
    user: UserResponse
    token: str