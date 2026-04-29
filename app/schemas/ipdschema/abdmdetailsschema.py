from pydantic import BaseModel
from typing import Optional

class AbdmDetailsBase(BaseModel):
    hfr_id: Optional[str] = None
    hpr_id: Optional[str] = None
    hip_publish_trigger: Optional[bool] = None
    record_linkage_status: Optional[str] = None

class AbdmDetailsCreate(AbdmDetailsBase):
    pass

class AbdmDetailsResponse(AbdmDetailsBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
