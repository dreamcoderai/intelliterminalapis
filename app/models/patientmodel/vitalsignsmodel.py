# app/models/patientmodel/vitalsignsmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base


class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("demographics.id")
    )
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)

    blood_pressure = Column(String(100))
    heart_rate = Column(String(100))
    spo2 = Column(String(100))
    temperature = Column(String(100))
    respiratory_rate = Column(String(100))
    blood_sugar = Column(String(100))
    weight_changes = Column(Text)

