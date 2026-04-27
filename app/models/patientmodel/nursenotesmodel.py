from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.core.database import Base


class NurseNote(Base):
    __tablename__ = "nurse_notes"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("demographics.id"), index=True)
    note_type = Column(String(50))   # vital_signs | observation | medication | general
    notes = Column(Text, default="")
    recorded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
