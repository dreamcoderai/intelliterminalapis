from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class ReferralDetails(Base):
    __tablename__ = "referral_details"
    
    id = Column(Integer, primary_key=True, index=True)
    admission_scheme_id = Column(Integer, ForeignKey("admission_scheme.id"))
    asha_anm_referral_id = Column(String(100))
    grievance_reference_id = Column(String(100))
