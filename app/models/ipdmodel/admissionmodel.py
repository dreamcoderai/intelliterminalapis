from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class IPDAdmission(Base):
    __tablename__ = "ipd_admissions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), index=True)
    visit_id = Column(String(50))
    admission_time = Column(DateTime(timezone=True), index=True)
    admission_type = Column(String(100))
    department = Column(String(100))
    status = Column(String(50))
    triage_level = Column(String(50))
    reason_for_admission = Column(Text)
    admitting_diagnosis_stem_code = Column(String(100))
    admitting_doctor_id = Column(Integer)
    attending_doctor_id = Column(Integer)
    created_by_user_id = Column(Integer)
    isolation_required = Column(Boolean, default=False)
    isolation_type = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
