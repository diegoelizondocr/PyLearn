FROM python:3.12-slim

# Evita que Python genere archivos .pyc y mejora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias primero (mejor cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ ./app/

# (Opcional pero recomendado) Crear usuario no-root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Exponer el puerto
EXPOSE 8000

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]