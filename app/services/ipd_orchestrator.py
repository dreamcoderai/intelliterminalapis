"""
ipd_orchestrator.py

Orchestrates the full flow of IPD Admission creation.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.ipdschema.fulladmissionschema import IPDFullAdmissionCreate, IPDFullAdmissionResponse

from app.services.admission_service import process_admission
from app.services.bed_service import process_bed_allocation
from app.services.transfer_service import process_transfer
from app.services.insurance_service import process_insurance

def create_full_admission(payload: IPDFullAdmissionCreate, db: Session) -> IPDFullAdmissionResponse:
    """
    Orchestrates the entire IPD admission process, managing the transaction lifecycle.
    Calls domain services sequentially and handles commit/rollback.

    Args:
        payload (IPDFullAdmissionCreate): The incoming admission payload.
        db (Session): SQLAlchemy database session.

    Returns:
        IPDFullAdmissionResponse: The structured response of the created admission.

    Raises:
        HTTPException: If any part of the admission flow fails.
    """
    try:
        # 1. Create Core Admission
        db_admission = process_admission(payload.basic, db)
        admission_id = db_admission.id
        patient_id = db_admission.patient_id

        # 2. Allocate Bed (Optional)
        response_bed = process_bed_allocation(payload.basic, patient_id, admission_id, db)

        # 3. Handle Transfer (Optional)
        response_transfer = process_transfer(payload.basic, patient_id, admission_id, db)

        # 4. Handle Insurance/Scheme (Optional)
        response_insurance = process_insurance(payload, patient_id, admission_id, db)

        # 5. Commit all changes atomically
        db.commit()

        return IPDFullAdmissionResponse(
            message="Admission created successfully",
            admission_id=admission_id,
            bed=response_bed,
            transfer=response_transfer,
            insurance=response_insurance,
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create admission: {str(e)}"
        )
