from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class BedAllocation(Base):
    __tablename__ = "bed_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"))
    bed_no = Column(String(50))
    bed_type = Column(String(100))
    ward_entitlement_class = Column(String(100))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
