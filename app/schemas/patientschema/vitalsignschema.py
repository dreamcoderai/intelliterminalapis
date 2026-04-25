# app/schemas/patientschema/vitalsignschema.py
from pydantic import BaseModel

class VitalSignsSchema(BaseModel):
    blood_pressure: str | None = None
    heart_rate: str | None = None
    spo2: str | None = None
    temperature: str | None = None
    respiratory_rate: str | None = None
    blood_sugar: str | None = None
    weight_changes: str | None = None

    class Config:
        orm_mode = True