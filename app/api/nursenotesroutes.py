from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.patientmodel.demographicmodel import Demographic
from app.models.patientmodel.nursenotesmodel import NurseNote

nursenotesrouter = APIRouter(prefix="/nurse-notes", tags=["Nurse Notes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _serialize(row: NurseNote) -> dict:
    return {
        "id":          row.id,
        "patient_id":  row.patient_id,
        "note_type":   row.note_type,
        "notes":       row.notes or "",
        "recorded_at": row.recorded_at.isoformat() if row.recorded_at else None,
    }


class NurseNoteIn(BaseModel):
    patient_id: int
    note_type: str   # vital_signs | observation | medication | general
    notes: str = ""


@nursenotesrouter.get("/")
def list_nurse_notes(patient_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(NurseNote)
    if patient_id is not None:
        query = query.filter(NurseNote.patient_id == patient_id)
    return [_serialize(r) for r in query.order_by(NurseNote.recorded_at.desc()).all()]


@nursenotesrouter.post("/")
def create_nurse_note(body: NurseNoteIn, db: Session = Depends(get_db)):
    if not db.query(Demographic).filter(Demographic.id == body.patient_id).first():
        raise HTTPException(status_code=404, detail="Patient not found")
    row = NurseNote(
        patient_id=body.patient_id,
        note_type=body.note_type,
        notes=body.notes,
        recorded_at=datetime.now(timezone.utc),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _serialize(row)


@nursenotesrouter.delete("/{note_id}")
def delete_nurse_note(note_id: int, db: Session = Depends(get_db)):
    row = db.query(NurseNote).filter(NurseNote.id == note_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(row)
    db.commit()
    return {"ok": True}
