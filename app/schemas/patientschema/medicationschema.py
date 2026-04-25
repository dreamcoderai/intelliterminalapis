# app/schemas/patientschema/medicationschema.py
from pydantic import BaseModel

class MedicationsSchema(BaseModel):
    current_medicines: str | None = None
    dosage: str | None = None
    frequency: str | None = None
    start_date: str | None = None
    stop_date: str | None = None
    medication_adherence: str | None = None
    side_effects: str | None = None

    class Config:
        orm_mode = True