# app/schemas/patientschema/lifestyledataschema.py
from pydantic import BaseModel

class LifestyleDataSchema(BaseModel):
    smoking: str | None = None
    alcohol: str | None = None
    exercise_habits: str | None = None
    diet: str | None = None
    sleep_quality: str | None = None
    stress_levels: str | None = None

    class Config:
        orm_mode = True