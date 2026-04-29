from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CghsDetailsBase(BaseModel):
    cghs_card_number: Optional[str] = None
    cghs_city_region: Optional[str] = None
    cghs_referral_id: Optional[str] = None
    cghs_referral_validity_date: Optional[datetime] = None
    referring_mo_id: Optional[str] = None
    cghs_beneficiary_category: Optional[str] = None
    endorsed_investigation_flag: Optional[bool] = None
    report_back_flag: Optional[bool] = None

class CghsDetailsCreate(CghsDetailsBase):
    pass

class CghsDetailsResponse(CghsDetailsBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
