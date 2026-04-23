# app/schemas/patientschema/remotemonitoringschema.py
from pydantic import BaseModel

class RemoteMonitoringSchema(BaseModel):
    smartwatch_heart_rate: str | None = None

    class Config:
        orm_mode = True
