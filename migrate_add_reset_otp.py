"""One-shot migration: add reset_otp and reset_otp_expiry columns to users table."""

from app.core.database import SessionLocal

SQL = [
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_otp VARCHAR;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_otp_expiry TIMESTAMP;",
]

db = SessionLocal()
try:
    for stmt in SQL:
        db.execute(__import__("sqlalchemy").text(stmt))
    db.commit()
    print("Migration complete.")
finally:
    db.close()
