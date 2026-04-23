# app/schemas/patientschema/lifestyledataschema.py
from pydantic import BaseModel

class LifestyleDataSchema(BaseModel):
    smoking: str | None = None
    alcohol: str | None = None

    class Config:
        orm_mode = True