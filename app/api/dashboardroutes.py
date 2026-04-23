# app/api/dashboard_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.usersmodel.usermodel import User

dashboardrouter = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
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
# Dashboard Summary API
# Returns ARRAY for React stats.map()
# -----------------------------------
@dashboardrouter.get("/")
def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """
    Dashboard Summary API

    Returns array format for frontend:

    [
        {
            "title": "Total Users",
            "value": 10
        }
    ]
    """

    total_users = db.query(User).count()

    total_doctors = db.query(User).filter(
        User.role == "doctor"
    ).count()

    total_executives = db.query(User).filter(
        User.role == "executive"
    ).count()

    total_admins = db.query(User).filter(
        User.role == "admin"
    ).count()

    active_users = db.query(User).filter(
        User.is_active == True
    ).count()

    return [
        {
            "title": "Total Users",
            "value": total_users
        },
        {
            "title": "Doctors",
            "value": total_doctors
        },
        {
            "title": "Executives",
            "value": total_executives
        },
        {
            "title": "Admins",
            "value": total_admins
        },
        {
            "title": "Active Users",
            "value": active_users
        }
    ]


# -----------------------------------
# Role Summary API
# -----------------------------------
@dashboardrouter.get("/role-summary")
def get_role_summary(
    db: Session = Depends(get_db)
):
    """
    Role-wise Summary API
    """

    total_doctors = db.query(User).filter(
        User.role == "doctor"
    ).count()

    total_executives = db.query(User).filter(
        User.role == "executive"
    ).count()

    total_admins = db.query(User).filter(
        User.role == "admin"
    ).count()

    return [
        {
            "role": "doctor",
            "count": total_doctors
        },
        {
            "role": "executive",
            "count": total_executives
        },
        {
            "role": "admin",
            "count": total_admins
        }
    ]