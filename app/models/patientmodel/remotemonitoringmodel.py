# app/models/patientmodel/remotemonitoringmodel.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class RemoteMonitoring(Base):
    __tablename__ = "remote_monitoring"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)
    smartwatch_heart_rate = Column(Text)
    ecg_patches = Column(Text)
    glucose_monitors = Column(Text)
    bp_machine = Column(Text)
    fitness_tracker = Column(Text)
    sleep_tracker = Column(Text)
