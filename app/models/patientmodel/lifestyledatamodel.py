
# app/models/patientmodel/lifestyledatamodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class LifestyleData(Base):
    __tablename__ = "lifestyle_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)
    smoking = Column(String(100))
    alcohol = Column(String(100))
    exercise_habits = Column(Text)
    diet = Column(Text)
    sleep_quality = Column(Text)
    stress_levels = Column(Text)