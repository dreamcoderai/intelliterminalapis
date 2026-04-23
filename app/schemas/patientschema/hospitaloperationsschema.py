# app/schemas/patientschema/hospitaloperationsschema.py
from pydantic import BaseModel

class HospitalOperationsSchema(BaseModel):
    admission_history: str | None = None
    icu_stay: str | None = None

    class Config:
        orm_mode = True