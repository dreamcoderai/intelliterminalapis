from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BedAllocationBase(BaseModel):
    bed_no: str
    bed_type: Optional[str] = None
    ward_entitlement_class: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None

class BedAllocationCreate(BedAllocationBase):
    pass

class BedAllocationResponse(BedAllocationBase):
    id: int
    patient_id: int
    ipd_admission_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
