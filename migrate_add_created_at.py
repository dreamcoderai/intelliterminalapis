"""Add created_at to users table."""
import sqlalchemy
from app.core.database import SessionLocal

db = SessionLocal()
try:
    db.execute(sqlalchemy.text(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();"
    ))
    db.commit()
    print("Migration complete.")
finally:
    db.close()
