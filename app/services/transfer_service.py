"""
transfer_service.py

Handles transfer details for an IPD Admission.
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.ipdmodel.admissiontransfermodel import AdmissionTransfer

def process_transfer(basic_payload: object, patient_id: int, admission_id: int, db: Session) -> Optional[Dict[str, Any]]:
    """
    Creates an AdmissionTransfer record if transfer details are provided.

    Args:
        basic_payload: The basic admission data containing transfer details.
        patient_id (int): The ID of the patient.
        admission_id (int): The ID of the IPD admission.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing transfer details, or None if no transfer details were provided.
    """
    if not basic_payload.transfer_from_facility:
        return None

    db_transfer = AdmissionTransfer(
        patient_id=patient_id,
        ipd_admission_id=admission_id,
        transfer_from_facility=basic_payload.transfer_from_facility,
        transfer_reason=basic_payload.transfer_reason,
    )
    db.add(db_transfer)
    db.flush()

    return {
        "id": db_transfer.id,
        "transfer_from_facility": basic_payload.transfer_from_facility,
        "transfer_reason": basic_payload.transfer_reason,
    }
