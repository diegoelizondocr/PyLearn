from loguru import logger
import sys

def setup_logging():
    # Elimina el handler por defecto
    logger.remove()

    # Logs a consola (colores + formato bonito)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )

    # Logs a archivo (opcional)
    logger.add(
        "logs/api_{time:YYYY-MM-DD}.log",
        rotation="10 MB",      # nuevo archivo cada 10 MB
        retention="15 days",   # guarda 15 días
        compression="zip",     # comprime los viejos
        level="DEBUG"
    )