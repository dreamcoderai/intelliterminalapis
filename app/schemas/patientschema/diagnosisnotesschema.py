# app/schemas/patientschema/diagnosisnotesschema.py
from pydantic import BaseModel

class DiagnosisNotesSchema(BaseModel):
    diagnosis_history: str | None = None
    doctor_notes: str | None = None

    class Config:
        orm_mode = True