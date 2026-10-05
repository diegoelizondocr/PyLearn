import oracledb
from contextlib import contextmanager
from app.config import settings

@contextmanager
def get_connection():
    conn = oracledb.connect(
        user=settings.oracle_user,
        password=settings.oracle_password,
        dsn=settings.oracle_dsn
    )
    try:
        yield conn
    finally:
        conn.close()


def get_db():
    """Dependency para FastAPI"""
    with get_connection() as conn:
        yield conn