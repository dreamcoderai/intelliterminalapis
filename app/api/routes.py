# app/api/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
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
            "is_active": existing_user.is_active
        },
        "token": "sample-jwt-token"
    }