from pydantic import BaseModel
from typing import Optional

class PmjayDetailsBase(BaseModel):
    pmjay_beneficiary_id: Optional[str] = None
    pmjay_family_id: Optional[str] = None
    scheme_beneficiary_category: Optional[str] = None
    pmjay_package_code: Optional[str] = None
    pre_auth_number: Optional[str] = None
    bio_auth_flag: Optional[bool] = None
    bio_auth_mode: Optional[str] = None
    arogya_mitra_id: Optional[str] = None
    tms_claim_id: Optional[str] = None
    cashless_vs_reimbursement: Optional[str] = None

class PmjayDetailsCreate(PmjayDetailsBase):
    pass

class PmjayDetailsResponse(PmjayDetailsBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
