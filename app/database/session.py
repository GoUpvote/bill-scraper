from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from .config import settings
import logging
import time
import socket
import os

logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    connect_args={
        'connect_timeout': 60,
    },
    echo=True
)
max_retries = 3
retry_delay = 5

for attempt in range(max_retries):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            break
    except Exception as e:
        logger.error(f"Connection error details: {type(e).__name__}: {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            logger.error("All connection attempts failed")
            raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Session:
    """
    Context manager for database sessions
    Usage:
        with get_db() as db:
            db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()