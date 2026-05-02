from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class PmjayDetails(Base):
    __tablename__ = "pmjay_details"
    
    id = Column(Integer, primary_key=True, index=True)
    admission_scheme_id = Column(Integer, ForeignKey("admission_scheme.id"))
    pmjay_beneficiary_id = Column(String(100))
    pmjay_family_id = Column(String(100))
    scheme_beneficiary_category = Column(String(100))
    pmjay_package_code = Column(String(100))
    pre_auth_number = Column(String(100))
    bio_auth_flag = Column(Boolean)
    bio_auth_mode = Column(String(50))
    arogya_mitra_id = Column(String(100))
    tms_claim_id = Column(String(100))
    cashless_vs_reimbursement = Column(String(50))
