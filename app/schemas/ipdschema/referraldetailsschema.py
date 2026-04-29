from pydantic import BaseModel
from typing import Optional

class ReferralDetailsBase(BaseModel):
    asha_anm_referral_id: Optional[str] = None
    grievance_reference_id: Optional[str] = None

class ReferralDetailsCreate(ReferralDetailsBase):
    pass

class ReferralDetailsResponse(ReferralDetailsBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
