# app/schemas/patientschema/medicationschema.py
from pydantic import BaseModel

class MedicationsSchema(BaseModel):
    current_medicines: str | None = None
    dosage: str | None = None
    frequency: str | None = None

    class Config:
        orm_mode = True