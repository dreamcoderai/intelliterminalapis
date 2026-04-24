# app/schemas/patientschema/diagnosisnotesschema.py
from pydantic import BaseModel

class DiagnosisNotesSchema(BaseModel):
    diagnosis_history: str | None = None
    doctor_notes: str | None = None
    symptoms_progression: str | None = None
    follow_up_notes: str | None = None
    treatment_plan: str | None = None
    patient_symptoms: str | None = None
    symptom_tokens: str | None = None

    class Config:
        orm_mode = True
