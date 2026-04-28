"""Add extracted_texts column to imaging_data table."""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pulseadmin:pulse123@localhost:5432/pulseterminal")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

cur.execute("""
    ALTER TABLE imaging_data
    ADD COLUMN IF NOT EXISTS extracted_texts TEXT;
""")

print("OK: extracted_texts column added to imaging_data")

cur.close()
conn.close()
