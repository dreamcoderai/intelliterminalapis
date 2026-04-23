# app/models/patientmodel/demographicmodel.py

from sqlalchemy import Column, Integer, String, Text
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
    contact_details = Column(Text)
    emergency_contact = Column(String(255))
    insurance_details = Column(Text)