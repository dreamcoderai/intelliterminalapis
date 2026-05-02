"""
insurance_service.py

Handles insurance and scheme linkage for an IPD Admission.
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.ipdmodel.admissionschememodel import AdmissionScheme
from app.models.ipdmodel.pmjaydetailsmodel import PmjayDetails
from app.models.ipdmodel.cghsdetailsmodel import CghsDetails
from app.models.ipdmodel.esicdetailsmodel import EsicDetails
from app.models.ipdmodel.abdmdetailsmodel import AbdmDetails
from app.models.ipdmodel.referraldetailsmodel import ReferralDetails
from app.schemas.ipdschema.fulladmissionschema import IPDFullAdmissionCreate

# Scheme model map for dynamic insertion
SCHEME_MODEL_MAP = {
    "pmjay": PmjayDetails,
    "cghs": CghsDetails,
    "esic": EsicDetails,
    "abdm": AbdmDetails,
    "referral": ReferralDetails,
}

def process_insurance(payload: IPDFullAdmissionCreate, patient_id: int, admission_id: int, db: Session) -> Optional[Dict[str, Any]]:
    """
    Creates an AdmissionScheme and its corresponding detail record.
    Allows only one active scheme by iterating over potential scheme sources and returning after the first valid match.

    Args:
        payload (IPDFullAdmissionCreate): The full admission payload containing potential scheme data.
        patient_id (int): The ID of the patient.
        admission_id (int): The ID of the IPD admission.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the active scheme details, or None if no scheme was provided.
    """
    scheme_sources = {
        "pmjay": payload.pmjay,
        "cghs": payload.cghs,
        "esic": payload.esic,
        "abdm": payload.abdm,
        "referral": payload.referral,
    }

    for scheme_name, scheme_data in scheme_sources.items():
        if scheme_data is None:
            continue

        # Skip empty dicts — frontend sends {} for inactive schemes
        detail_data = scheme_data.dict(exclude_none=True)
        if not detail_data:
            continue

        # Create the AdmissionScheme parent row
        db_scheme = AdmissionScheme(
            ipd_admission_id=admission_id,
            patient_id=patient_id,
            scheme_type=scheme_name.upper(),
        )
        db.add(db_scheme)
        db.flush()

        # For ABDM, also pull hfr_id from basic if not in scheme payload
        if scheme_name == "abdm" and "hfr_id" not in detail_data and payload.basic.hfr_id:
            detail_data["hfr_id"] = payload.basic.hfr_id

        # Insert scheme detail record
        model_cls = SCHEME_MODEL_MAP[scheme_name]
        db_detail = model_cls(admission_scheme_id=db_scheme.id, **detail_data)
        db.add(db_detail)
        db.flush()

        return {
            "active_scheme": scheme_name,
            "details": detail_data,
        }

    return None
