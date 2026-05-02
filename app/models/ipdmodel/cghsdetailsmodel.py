from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.core.database import Base

class CghsDetails(Base):
    __tablename__ = "cghs_details"
    
    id = Column(Integer, primary_key=True, index=True)
    admission_scheme_id = Column(Integer, ForeignKey("admission_scheme.id"))
    cghs_card_number = Column(String(100))
    cghs_city_region = Column(String(100))
    cghs_referral_id = Column(String(100))
    cghs_referral_validity_date = Column(DateTime(timezone=True))
    referring_mo_id = Column(String(100))
    cghs_beneficiary_category = Column(String(100))
    endorsed_investigation_flag = Column(Boolean)
    report_back_flag = Column(Boolean)
