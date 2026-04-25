# app/schemas/patientschema/remotemonitoringschema.py
from pydantic import BaseModel

class RemoteMonitoringSchema(BaseModel):
    smartwatch_heart_rate: str | None = None
    ecg_patches: str | None = None
    glucose_monitors: str | None = None
    bp_machine: str | None = None
    fitness_tracker: str | None = None
    sleep_tracker: str | None = None

    class Config:
        orm_mode = True
