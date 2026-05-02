"""Add gender and age columns to users table."""
import psycopg2

conn = psycopg2.connect("postgresql://pulseadmin:pulse123@localhost:5432/pulseterminal")
conn.autocommit = True
cur = conn.cursor()

cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(20);")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS age INTEGER;")

print("OK: gender and age columns added to users table")
cur.close()
conn.close()
