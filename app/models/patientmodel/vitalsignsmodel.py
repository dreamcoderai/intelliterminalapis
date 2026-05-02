# app/models/patientmodel/vitalsignsmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from app.core.database import Base


class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("demographics.id")
    )

    name = Column(String(100))
    unit = Column(String(50))
    value = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
