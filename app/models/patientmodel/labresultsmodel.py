# app/models/patientmodel/labresultsmodel.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base
class LabResults(Base):
    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    cbc = Column(Text)
    hba1c = Column(Text)
    lipid_profile = Column(Text)
    liver_function = Column(Text)
    kidney_function = Column(Text)
    thyroid_profile = Column(Text)
    vitamin_levels = Column(Text)
    ecg_echo_reports = Column(Text)