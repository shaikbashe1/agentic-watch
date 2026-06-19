from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

# Use DATABASE_URL from environment, or fallback to the local postgres container
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost/agentwatch")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
