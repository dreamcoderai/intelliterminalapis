from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .bedallocationschema import BedAllocationResponse
from .admissionschemeschema import AdmissionSchemeResponse
from .admissiontransferschema import AdmissionTransferResponse

class IPDAdmissionBase(BaseModel):
    patient_id: int
    visit_id: Optional[str] = None
    admission_time: datetime
    admission_type: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None
    triage_level: Optional[str] = None
    reason_for_admission: Optional[str] = None
    admitting_diagnosis_stem_code: Optional[str] = None
    admitting_doctor_id: Optional[int] = None
    attending_doctor_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    filled_by_role: Optional[str] = None
    # Bed fields (sent flat in basic)
    bed_no: Optional[str] = None
    bed_type: Optional[str] = None
    ward_entitlement_class: Optional[str] = None
    isolation_required: Optional[bool] = None
    isolation_type: Optional[str] = None
    # Transfer fields (sent flat in basic)
    transfer_from_facility: Optional[str] = None
    transfer_reason: Optional[str] = None
    # ABDM / HFR
    hfr_id: Optional[str] = None

class IPDAdmissionCreate(IPDAdmissionBase):
    patient_id: int

class IPDAdmissionResponse(IPDAdmissionBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class IPDAdmissionTimeline(IPDAdmissionResponse):
    bed_allocations: List[BedAllocationResponse] = []
    admission_scheme: Optional[AdmissionSchemeResponse] = None
    transfers: List[AdmissionTransferResponse] = []
