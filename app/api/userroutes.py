# app/api/user_routes.py

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.storage import delete_patient_files, upload_user_file
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
# List Users API
# GET /users/?role=doctor
# --------------------------------------------------

@userrouter.get("/", response_model=list[UserResponse])
def list_users(
    role: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if search:
        q = f"%{search}%"
        query = query.filter(
            User.name.ilike(q) | User.email.ilike(q) | User.department.ilike(q)
        )
    return query.order_by(User.name).offset(skip).limit(limit).all()


# --------------------------------------------------
# Delete User API
# DELETE /users/{user_id}
# --------------------------------------------------

@userrouter.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.profile_pic:
        delete_patient_files([user.profile_pic])
    db.delete(user)
    db.commit()


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
        gender=payload.gender,
        dob=payload.dob,
        is_active=payload.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# --------------------------------------------------
# Get User Profile
# GET /users/{user_id}
# --------------------------------------------------

@userrouter.get("/{user_id}", response_model=UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --------------------------------------------------
# Update User Profile
# PUT /users/{user_id}
# Accepts multipart form data so profile pic can be uploaded
# --------------------------------------------------

@userrouter.put("/{user_id}", response_model=UserResponse)
def update_profile(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(""),
    phone: str = Form(""),
    gender: str = Form(""),
    age: str = Form(""),
    dob: str = Form(""),
    profile_pic: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = name
    user.email = email
    user.department = department or None
    user.phone = phone or None
    user.gender = gender or None
    user.age = int(age) if age.strip().isdigit() else None
    user.dob = dob or None

    if profile_pic and profile_pic.filename:
        if user.profile_pic:
            delete_patient_files([user.profile_pic])
        user.profile_pic = upload_user_file(profile_pic, user_id)

    db.commit()
    db.refresh(user)
    return user