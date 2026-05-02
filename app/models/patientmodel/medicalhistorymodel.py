# app/models/patientmodel/medicalhistorymodel.py

from sqlalchemy import Column, Integer, Text, ForeignKey
from app.core.database import Base


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    past_illnesses = Column(Text)
    surgeries = Column(Text)
    chronic_diseases = Column(Text)
    family_history = Column(Text)
    allergies = Column(Text)
    previous_hospitalizations = Column(Text)
    vaccination_history = Column(Text)
    social_history = Column(Text)