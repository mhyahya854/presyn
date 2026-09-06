from __future__ import annotations
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings

def ensure_data_directory(database_url: str) -> None:
    if database_url.startswith('sqlite:///'):
        file_path = database_url.replace('sqlite:///', '')
        if file_path and not file_path.startswith(':memory:'):
            parent_dir = Path(file_path).resolve().parent
            parent_dir.mkdir(parents=True, exist_ok=True)

ensure_data_directory(settings.DATABASE_URL)
connect_args = {}
if settings.DATABASE_URL.startswith('sqlite'):
    connect_args['check_same_thread'] = False

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, echo=False, future=True)

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if settings.DATABASE_URL.startswith('sqlite'):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
