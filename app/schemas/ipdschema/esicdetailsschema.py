from pydantic import BaseModel
from typing import Optional

class EsicDetailsBase(BaseModel):
    esic_ip_number: Optional[str] = None
    esic_dhanwantari_slip_id: Optional[str] = None
    employer_code: Optional[str] = None
    contribution_period_validity_flag: Optional[bool] = None

class EsicDetailsCreate(EsicDetailsBase):
    pass

class EsicDetailsResponse(EsicDetailsBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
