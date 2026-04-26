# app/api/dashboardroutes.py

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.patientmodel.demographicmodel import Demographic
from app.models.usersmodel.usermodel import User

dashboardrouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── helpers ────────────────────────────────────────────────────────────────────

MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def last_6_months():
    """Return list of (year, month) tuples for the last 6 months, oldest first."""
    now = datetime.now(timezone.utc)
    months = []
    for i in range(5, -1, -1):
        dt = now - timedelta(days=30 * i)
        months.append((dt.year, dt.month))
    return months


# ── main stats endpoint ────────────────────────────────────────────────────────

@dashboardrouter.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    # ── counts ────────────────────────────────────────────────────────────────
    users      = db.query(User).all()
    patients   = db.query(Demographic).all()

    doctors    = [u for u in users if u.role == "doctor"]
    executives = [u for u in users if u.role == "executive"]
    active     = [u for u in users if u.is_active]

    # ── monthly registrations (last 6 months) ────────────────────────────────
    months = last_6_months()
    user_by_month    = defaultdict(int)
    patient_by_month = defaultdict(int)

    staff = doctors + executives
    for u in staff:
        if u.created_at:
            key = (u.created_at.year, u.created_at.month)
            if key in months:
                user_by_month[key] += 1

    for p in patients:
        if p.created_at:
            ts = p.created_at
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            key = (ts.year, ts.month)
            if key in [(y, m) for y, m in months]:
                patient_by_month[key] += 1

    monthly = [
        {
            "month": MONTH_LABELS[m - 1],
            "users": user_by_month[(y, m)],
            "patients": patient_by_month[(y, m)],
        }
        for y, m in months
    ]

    # ── weekly patient registrations (last 7 days) ────────────────────────────
    today = datetime.now(timezone.utc).date()
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_counts = defaultdict(int)

    for p in patients:
        if p.created_at:
            ts = p.created_at
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            delta = (today - ts.date()).days
            if 0 <= delta < 7:
                day_counts[ts.strftime("%a")] += 1

    weekly = [{"day": d, "registrations": day_counts.get(d, 0)} for d in day_labels]

    # ── blood group distribution ──────────────────────────────────────────────
    bg_counts = defaultdict(int)
    for p in patients:
        if p.blood_group:
            bg_counts[p.blood_group.strip()] += 1

    blood_groups = [{"name": k, "value": v} for k, v in sorted(bg_counts.items())]

    # ── gender distribution ───────────────────────────────────────────────────
    gender_counts = defaultdict(int)
    for p in patients:
        if p.gender:
            gender_counts[p.gender.strip().capitalize()] += 1

    gender = [{"name": k, "value": v} for k, v in gender_counts.items()]

    # ── active vs inactive ────────────────────────────────────────────────────
    active_split = [
        {"name": "Active",   "value": len(active),             "fill": "#10b981"},
        {"name": "Inactive", "value": len(users) - len(active), "fill": "#ef4444"},
    ]

    # ── recent patients ───────────────────────────────────────────────────────
    recent = sorted(
        [p for p in patients if p.created_at],
        key=lambda p: p.created_at,
        reverse=True,
    )[:5]

    recent_patients = [
        {
            "id": p.id,
            "full_name": p.full_name,
            "blood_group": p.blood_group,
            "gender": p.gender,
            "age": p.age,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in recent
    ]

    # ── department breakdown (doctors only) ───────────────────────────────────
    dept_counts = defaultdict(int)
    for u in doctors:
        dept_counts[u.department or "General"] += 1

    departments = [{"name": k, "value": v} for k, v in sorted(dept_counts.items(), key=lambda x: -x[1])]

    return {
        "counts": {
            "total_users": len(doctors) + len(executives) + len(patients),
            "doctors": len(doctors),
            "executives": len(executives),
            "patients": len(patients),
            "active_users": len(active),
        },
        "monthly_registrations": monthly,
        "weekly_patient_registrations": weekly,
        "blood_group_distribution": blood_groups,
        "gender_distribution": gender,
        "active_split": active_split,
        "recent_patients": recent_patients,
        "departments": departments,
    }


# ── legacy endpoints (kept for compatibility) ──────────────────────────────────

@dashboardrouter.get("/")
def get_dashboard_data(db: Session = Depends(get_db)):
    total_users      = db.query(User).count()
    total_doctors    = db.query(User).filter(User.role == "doctor").count()
    total_executives = db.query(User).filter(User.role == "executive").count()
    total_admins     = db.query(User).filter(User.role == "admin").count()
    active_users     = db.query(User).filter(User.is_active == True).count()
    return [
        {"title": "Total Users",  "value": total_users},
        {"title": "Doctors",      "value": total_doctors},
        {"title": "Executives",   "value": total_executives},
        {"title": "Admins",       "value": total_admins},
        {"title": "Active Users", "value": active_users},
    ]


@dashboardrouter.get("/role-summary")
def get_role_summary(db: Session = Depends(get_db)):
    return [
        {"role": "doctor",    "count": db.query(User).filter(User.role == "doctor").count()},
        {"role": "executive", "count": db.query(User).filter(User.role == "executive").count()},
        {"role": "admin",     "count": db.query(User).filter(User.role == "admin").count()},
    ]
