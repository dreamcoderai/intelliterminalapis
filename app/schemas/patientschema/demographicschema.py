
# app/schemas/patientschema/demographicschema.py

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
    contact_details: str
    emergency_contact: str
    insurance_details: str


class DemographicResponse(DemographicCreate):
    id: int

    class Config:
        orm_mode = True