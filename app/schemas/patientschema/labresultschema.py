
# app/schemas/patientschema/labresultschema.py
from pydantic import BaseModel

class LabResultsSchema(BaseModel):
    cbc: str | None = None
    hba1c: str | None = None
    lipid_profile: str | None = None

    class Config:
        orm_mode = True