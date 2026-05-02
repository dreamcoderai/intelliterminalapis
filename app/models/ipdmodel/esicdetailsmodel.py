from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class EsicDetails(Base):
    __tablename__ = "esic_details"
    
    id = Column(Integer, primary_key=True, index=True)
    admission_scheme_id = Column(Integer, ForeignKey("admission_scheme.id"))
    esic_ip_number = Column(String(100))
    esic_dhanwantari_slip_id = Column(String(100))
    employer_code = Column(String(100))
    contribution_period_validity_flag = Column(Boolean)
