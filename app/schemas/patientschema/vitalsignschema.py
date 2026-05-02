# app/schemas/patientschema/vitalsignschema.py
from pydantic import BaseModel
from datetime import datetime

class VitalSignsSchema(BaseModel):
    name: str | None = None
    unit: str | None = None
    value: str | None = None

    class Config:
        orm_mode = True