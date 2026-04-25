
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
    address: str
    emergency_contact: str
    insurance_details: str


class DemographicResponse(DemographicCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True