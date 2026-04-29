from pydantic import BaseModel

class AdmissionSchemeBase(BaseModel):
    scheme_type: str

class AdmissionSchemeCreate(AdmissionSchemeBase):
    pass

class AdmissionSchemeResponse(AdmissionSchemeBase):
    id: int
    ipd_admission_id: int
    patient_id: int
    class Config:
        from_attributes = True
