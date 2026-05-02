from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class AdmissionScheme(Base):
    __tablename__ = "admission_scheme"
    
    id = Column(Integer, primary_key=True, index=True)
    ipd_admission_id = Column(Integer, ForeignKey("ipd_admissions.id"), unique=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"))
    scheme_type = Column(String(50)) # PMJAY / CGHS / ESIC / PRIVATE / SELF
