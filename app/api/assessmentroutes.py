# app/api/assessmentroutes.py

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.patientmodel.demographicmodel import Demographic
from app.models.patientmodel.doctorassessmentmodel import DoctorAssessment

assessmentrouter = APIRouter(prefix="/assessments", tags=["Assessments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _serialize(row: DoctorAssessment) -> dict:
    return {
        "id":          row.id,
        "patient_id":  row.patient_id,
        "status":      row.status,
        "notes":       row.notes or "",
        "assessed_at": row.assessed_at.isoformat() if row.assessed_at else None,
    }


class AssessmentIn(BaseModel):
    patient_id: int
    status: str   # critical | normal | recovering
    notes: str = ""


@assessmentrouter.get("/")
def list_assessments(db: Session = Depends(get_db)):
    return [_serialize(r) for r in db.query(DoctorAssessment).all()]


@assessmentrouter.get("/{patient_id}")
def get_assessment(patient_id: int, db: Session = Depends(get_db)):
    row = db.query(DoctorAssessment).filter(
        DoctorAssessment.patient_id == patient_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="No assessment found")
    return _serialize(row)


@assessmentrouter.post("/")
def upsert_assessment(body: AssessmentIn, db: Session = Depends(get_db)):
    if not db.query(Demographic).filter(Demographic.id == body.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")

    now = datetime.now(timezone.utc)
    row = db.query(DoctorAssessment).filter(
        DoctorAssessment.patient_id == body.patient_id
    ).first()

    if row:
        row.status      = body.status
        row.notes       = body.notes
        row.assessed_at = now
    else:
        row = DoctorAssessment(
            patient_id=body.patient_id,
            status=body.status,
            notes=body.notes,
            assessed_at=now,
        )
        db.add(row)

    db.commit()
    db.refresh(row)
    return _serialize(row)
