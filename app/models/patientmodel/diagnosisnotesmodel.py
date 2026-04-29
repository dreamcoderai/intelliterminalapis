# app/models/patientmodel/diagnosisnotesmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class DiagnosisNotes(Base):
    __tablename__ = "diagnosis_notes"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)
    diagnosis_history = Column(Text)
    doctor_notes = Column(Text)
    symptoms_progression = Column(Text)
    follow_up_notes = Column(Text)
    treatment_plan = Column(Text)
    patient_symptoms = Column(Text)
    symptom_tokens = Column(Text)
