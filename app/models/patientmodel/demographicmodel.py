# app/models/patientmodel/demographicmodel.py

from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.core.database import Base


class Demographic(Base):
    __tablename__ = "demographics"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    dob = Column(String(100))
    age = Column(Integer)
    gender = Column(String(50))
    blood_group = Column(String(20))
    height = Column(String(50))
    weight = Column(String(50))
    bmi = Column(String(50))
    phone = Column(String(50))
    email = Column(String(255))
    address = Column(Text)
    emergency_contact = Column(String(255))
    insurance_details = Column(Text)
    address_line1 = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    pincode = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    marital_status = Column(String(50), nullable=False)
    alternate_number = Column(String(50), nullable=True)
    aadhaar_number = Column(String(20), nullable=False)
    abha_number = Column(String(50), nullable=True)
    abha_address = Column(String(255), nullable=True)
    scan_share_token_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())