# app/models/patientmodel/doctorassessmentmodel.py

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.core.database import Base


class DoctorAssessment(Base):
    __tablename__ = "doctor_assessments"

    id         = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"), unique=True, index=True)
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), nullable=True)
    status     = Column(String(50))   # critical | normal | recovering
    notes      = Column(Text, default="")
    assessed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
