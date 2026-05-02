# app/models/patientmodel/hospitaloperationsmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class HospitalOperations(Base):
    __tablename__ = "hospital_operations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)
    admission_history = Column(Text)
    icu_stay = Column(Text)
    opd_visits = Column(Text)
    readmission_risk = Column(Text)
    treatment_response = Column(Text)