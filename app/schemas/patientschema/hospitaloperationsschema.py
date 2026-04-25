# app/schemas/patientschema/hospitaloperationsschema.py
from pydantic import BaseModel

class HospitalOperationsSchema(BaseModel):
    admission_history: str | None = None
    icu_stay: str | None = None
    opd_visits: str | None = None
    readmission_risk: str | None = None
    treatment_response: str | None = None

    class Config:
        orm_mode = True