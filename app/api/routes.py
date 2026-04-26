# app/api/routes.py

import random
import string
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.email import send_otp_email
from app.models.usersmodel.usermodel import User
from app.schemas.usersschema.userschema import (
    UserLogin,
    UserLoginResponse
)

router = APIRouter(
    tags=["Authentication"]
)


# -----------------------------------
# Database Dependency
# -----------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------
# Root Health Check API
# -----------------------------------
@router.get("/")
def home():
    return {
        "message": "PulseTerminal API Running"
    }


# -----------------------------------
# Login API
# Admin / Doctor / Executive Login
# -----------------------------------
@router.post(
    "/auth/login",
    response_model=UserLoginResponse
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login API checks:

    1. Existing user by email
    2. Password validation
    3. Role-based login support

    Roles:
    - admin
    - doctor
    - executive
    """

    # Check if user exists
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Password validation
    # Later replace with hashed password check
    if existing_user.password != payload.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email,
            "role": existing_user.role,
            "department": existing_user.department,
            "phone": existing_user.phone,
            "is_active": existing_user.is_active,
            "profile_pic": existing_user.profile_pic,
        },
        "token": "sample-jwt-token"
    }


# -----------------------------------
# Forgot Password — send OTP
# POST /auth/forgot-password
# -----------------------------------

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


@router.post("/auth/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email.")

    otp = "".join(random.choices(string.digits, k=6))
    user.reset_otp = otp
    user.reset_otp_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.commit()

    try:
        send_otp_email(user.email, otp, user.name)
    except Exception as exc:
        # Roll back the OTP so the user can try again
        user.reset_otp = None
        user.reset_otp_expiry = None
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to send OTP email: {exc}") from exc

    return {"message": "OTP sent to your email address."}


# -----------------------------------
# Reset Password — verify OTP + set new password
# POST /auth/reset-password
# -----------------------------------

class ChangePasswordRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str


@router.post("/auth/change-password")
def change_password(payload: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.password != payload.current_password:
        raise HTTPException(status_code=401, detail="Current password is incorrect.")
    user.password = payload.new_password
    db.commit()
    return {"message": "Password changed successfully."}


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


@router.post("/auth/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.reset_otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    if user.reset_otp_expiry and datetime.utcnow() > user.reset_otp_expiry:
        user.reset_otp = None
        user.reset_otp_expiry = None
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    if user.reset_otp != payload.otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP.")

    user.password = payload.new_password
    user.reset_otp = None
    user.reset_otp_expiry = None
    db.commit()

    return {"message": "Password reset successfully."}