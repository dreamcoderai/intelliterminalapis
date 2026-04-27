# app/models/patientmodel/imagingdatamodel.py

from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.database import Base


class ImagingData(Base):
    __tablename__ = "imaging_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    xray = Column(String(500))
    ct_scan = Column(String(500))
    mri = Column(String(500))
    ultrasound = Column(String(500))
    dicom_images = Column(String(500))
    radiology_reports = Column(String(500))
    voice_url = Column(String(500), nullable=True)
