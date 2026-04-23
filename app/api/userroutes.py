# app/api/user_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.usersmodel.usermodel import User
from app.schemas.usersschema.userschema import UserCreate, UserResponse

userrouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# --------------------------------------------------
# DB Dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Create User API
# POST → Save into PostgreSQL
# --------------------------------------------------

@userrouter.post("/", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        name=payload.name,
        email=payload.email,
        password=payload.password,  # later hash this
        role=payload.role,
        department=payload.department,
        phone=payload.phone,
        is_active=payload.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user