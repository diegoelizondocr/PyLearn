from fastapi import FastAPI
from app.config import settings
from app.routers import email, users, roles
from app.database import get_connection
from app.logging_config import setup_logging
from loguru import logger

setup_logging()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version
)

# Registrar routers
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(email.router)


@app.get("/", tags=["System"])
def home():
    logger.info("Se accedió al endpoint raíz")
    return {"message": "Oracle API Running"}


@app.get("/health", tags=["System"])
def health_check():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM dual")
                cursor.fetchone()
        logger.info("Health check OK - Base de datos conectada")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "error", "detail": str(e)}