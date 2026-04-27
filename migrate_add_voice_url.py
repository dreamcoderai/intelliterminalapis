"""
One-shot migration: adds voice_url column to imaging_data table.
Run once: python migrate_add_voice_url.py
"""
from app.core.database import engine
from sqlalchemy import text

migrations = [
    """
    ALTER TABLE imaging_data
    ADD COLUMN IF NOT EXISTS voice_url TEXT;
    """,
]

with engine.connect() as conn:
    for sql in migrations:
        try:
            conn.execute(text(sql.strip()))
            print(f"OK: {sql.strip()[:60]}...")
        except Exception as e:
            print(f"SKIP (already applied or error): {e}")
    conn.commit()

print("\nMigration complete.")
