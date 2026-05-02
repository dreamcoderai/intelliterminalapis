from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdmissionTransferBase(BaseModel):
    transfer_from_facility: Optional[str] = None
    transfer_reason: Optional[str] = None

class AdmissionTransferCreate(AdmissionTransferBase):
    pass

class AdmissionTransferResponse(AdmissionTransferBase):
    id: int
    patient_id: int
    ipd_admission_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
