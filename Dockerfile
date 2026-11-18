
# ==========================================
# SMARTRECIPE AI - DOCKERFILE
# ==========================================

# Imagen base de Python
FROM python:3.12-slim

# Configuracion de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Carpeta de trabajo
WORKDIR /app

# Crear usuario sin privilegios root
RUN groupadd --system appgroup \
    && useradd --system \
    --gid appgroup \
    --home-dir /app \
    appuser

# Instalar dependencias
COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    -r requirements.txt

# Copiar backend, frontend y otros archivos
COPY --chown=appuser:appgroup . .

# Ejecutar como usuario no privilegiado
USER appuser

# Puerto interno de FastAPI
EXPOSE 8000

# Inicializar las tablas antes de aceptar solicitudes.
CMD ["sh", "-c", "python -m app.init_db && exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
