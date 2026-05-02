# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------
# PostgreSQL Connection String
# Format:
# postgresql://username:password@host:port/database
# --------------------------------------------------

DATABASE_URL = "postgresql://postgres:msadmin@localhost:5432/fluxion"

# --------------------------------------------------
# SQLAlchemy Engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL queries in terminal (good for development)
)

# --------------------------------------------------
# Session Local
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --------------------------------------------------
# Base Model
# --------------------------------------------------

Base = declarative_base()