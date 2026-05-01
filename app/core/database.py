# app/core/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME')}"
)

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