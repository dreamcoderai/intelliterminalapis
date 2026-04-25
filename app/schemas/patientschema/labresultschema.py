
# app/schemas/patientschema/labresultschema.py
from pydantic import BaseModel

class LabResultsSchema(BaseModel):
    cbc: str | None = None
    hba1c: str | None = None
    lipid_profile: str | None = None
    liver_function: str | None = None
    kidney_function: str | None = None
    thyroid_profile: str | None = None
    vitamin_levels: str | None = None
    ecg_echo_reports: str | None = None

    class Config:
        orm_mode = True