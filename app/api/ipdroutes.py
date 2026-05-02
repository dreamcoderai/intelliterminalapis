from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.ipdschema.fulladmissionschema import (
    IPDFullAdmissionCreate,
    IPDFullAdmissionResponse,
)
from app.services.ipd_orchestrator import create_full_admission

router = APIRouter(
    prefix="/ipd",
    tags=["IPD"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/admission",
    response_model=IPDFullAdmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create IPD Admission",
    description="""Create a complete IPD admission record.
    """,
)
def create_unified_ipd_admission(payload: IPDFullAdmissionCreate, db: Session = Depends(get_db)) -> IPDFullAdmissionResponse:
    """
    Handles creation of a full IPD admission.
    """
    return create_full_admission(payload, db)    