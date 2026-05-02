from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class AdmissionTransfer(Base):
    __tablename__ = "admission_transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"))
    transfer_from_facility = Column(String(255))
    transfer_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
