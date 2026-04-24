# app/schemas/patientschema/imagingdataschema.py

from pydantic import BaseModel


class ImagingDataSchema(BaseModel):
    xray: str | None = None
    ct_scan: str | None = None
    mri: str | None = None
    ultrasound: str | None = None
    dicom_images: str | None = None
    radiology_reports: str | None = None

    class Config:
        orm_mode = True
