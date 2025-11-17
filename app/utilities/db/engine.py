from __future__ import annotations
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from app.utilities.config import get_settings

_engine: Engine | None = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        s = get_settings()
        url = f"postgresql+psycopg2://{s.pg_user}:{s.pg_password}@{s.pg_host}:{s.pg_port}/{s.pg_database}"
        _engine = create_engine(url, pool_pre_ping=True, future=True)
    return _engine

@contextmanager
def read_only_conn():
    eng = get_engine()
    with eng.connect() as conn:
        conn.execute(text("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY"))
        yield conn

def ping() -> bool:
    try:
        with read_only_conn() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
