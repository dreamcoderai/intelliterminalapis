
# app/schemas/patientschema/demographicschema.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DemographicCreate(BaseModel):
    full_name: str
    dob: str
    age: int
    gender: str
    blood_group: str
    height: str
    weight: str
    bmi: str
    phone: str
    email: str
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    insurance_details: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    village: Optional[str] = None
    block: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    marital_status: Optional[str] = None
    alternate_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    abha_number: Optional[str] = None
    abha_address: Optional[str] = None
    scan_share_token_id: Optional[str] = None


class DemographicResponse(DemographicCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True