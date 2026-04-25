"""
One-shot migration: adds profile_pic column to users table.
Run once: python migrate_add_profile_pic.py
"""
from app.core.database import engine
from sqlalchemy import text

migrations = [
    # users table
    """
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS profile_pic TEXT;
    """,
    # demographics table (created_at + separate contact fields)
    """
    ALTER TABLE demographics
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();
    """,
    """
    ALTER TABLE demographics
    ADD COLUMN IF NOT EXISTS phone TEXT;
    """,
    """
    ALTER TABLE demographics
    ADD COLUMN IF NOT EXISTS email TEXT;
    """,
    """
    ALTER TABLE demographics
    ADD COLUMN IF NOT EXISTS address TEXT;
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
