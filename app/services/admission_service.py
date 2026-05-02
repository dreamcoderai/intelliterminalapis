"""
admission_service.py

Handles core IPD Admission creation logic.
"""
from sqlalchemy.orm import Session
from app.models.ipdmodel.admissionmodel import IPDAdmission

# Columns that live on IPDAdmission model
ADMISSION_FIELDS = {
    "patient_id", "visit_id", "admission_time", "admission_type",
    "department", "status", "triage_level", "reason_for_admission",
    "admitting_diagnosis_stem_code", "admitting_doctor_id",
    "attending_doctor_id", "created_by_user_id",
    "isolation_required", "isolation_type",
}

def process_admission(basic_payload: object, db: Session) -> IPDAdmission:
    """
    Creates an IPDAdmission record.

    Args:
        basic_payload: The basic admission data from the payload.
        db (Session): SQLAlchemy database session.

    Returns:
        IPDAdmission: The created and flushed admission record.
    """
    # Build IPDAdmission fields (only model-valid columns)
    admission_data = {k: v for k, v in basic_payload.dict().items() if k in ADMISSION_FIELDS}
    db_admission = IPDAdmission(**admission_data)
    db.add(db_admission)
    db.flush()
    return db_admission
