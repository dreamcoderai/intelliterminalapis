# app/schemas/patientschema/imagingdataschema.py

class ImagingDataSchema(BaseModel):
    xray: str | None = None
    ct_scan: str | None = None
    mri: str | None = None

    class Config:
        orm_mode = True