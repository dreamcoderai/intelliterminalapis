# app/models/patientmodel/medicationsmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Medications(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    current_medicines = Column(Text)
    dosage = Column(Text)
    frequency = Column(Text)
    start_date = Column(String(100))
    stop_date = Column(String(100))
    medication_adherence = Column(String(100))
    side_effects = Column(Text)