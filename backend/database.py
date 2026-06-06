import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None


def init_db() -> None:
    if engine is None:
        return

    from backend import models  # noqa: F401
    # Import models to trigger SQLAlchemy model registration before creating tables

    Base.metadata.create_all(bind=engine)


def get_db():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured; PostgreSQL persistence is disabled.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()