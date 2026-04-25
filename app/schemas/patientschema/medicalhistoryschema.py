# app/schemas/patientschema/medicalhistoryschema.py
from pydantic import BaseModel

class MedicalHistorySchema(BaseModel):
    past_illnesses: str | None = None
    surgeries: str | None = None
    chronic_diseases: str | None = None
    family_history: str | None = None
    allergies: str | None = None
    previous_hospitalizations: str | None = None
    vaccination_history: str | None = None

    class Config:
        orm_mode = True