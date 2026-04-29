"""
bed_service.py

Handles bed allocation logic for an IPD Admission.
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.ipdmodel.bedallocationmodel import BedAllocation

def process_bed_allocation(basic_payload: object, patient_id: int, admission_id: int, db: Session) -> Optional[Dict[str, Any]]:
    """
    Creates a BedAllocation record if bed details are provided.

    Args:
        basic_payload: The basic admission data containing bed details.
        patient_id (int): The ID of the patient.
        admission_id (int): The ID of the IPD admission.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing bed allocation details, or None if no bed was allocated.
    """
    if not basic_payload.bed_no:
        return None

    db_bed = BedAllocation(
        bed_no=basic_payload.bed_no,
        bed_type=basic_payload.bed_type or None,
        ward_entitlement_class=basic_payload.ward_entitlement_class or None,
        patient_id=patient_id,
        ipd_admission_id=admission_id,
        start_time=basic_payload.admission_time,
    )
    db.add(db_bed)
    db.flush()

    return {
        "id": db_bed.id,
        "bed_no": basic_payload.bed_no,
        "bed_type": basic_payload.bed_type,
        "ward_entitlement_class": basic_payload.ward_entitlement_class,
    }
