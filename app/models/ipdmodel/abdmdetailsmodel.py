from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class AbdmDetails(Base):
    __tablename__ = "abdm_details"
    
    id = Column(Integer, primary_key=True, index=True)
    admission_scheme_id = Column(Integer, ForeignKey("admission_scheme.id"))
    hfr_id = Column(String(100))
    hpr_id = Column(String(100))
    hip_publish_trigger = Column(Boolean)
    record_linkage_status = Column(String(50))
