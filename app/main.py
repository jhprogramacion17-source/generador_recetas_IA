
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine

from app.routers.auth import (
    router as auth_router
)

from app.routers.ingredientes import (
    router as ingredientes_router
)

from app.routers.recetas import (
    router as recetas_router
)


# =====================================
# CONFIGURACION DE FASTAPI
# =====================================

app = FastAPI(
    title="SmartRecipe AI",
    description=(
        "API REST para gestionar ingredientes "
        "y generar recetas con inteligencia artificial"
    ),
    version="1.0.0"
)


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# REGISTRO DE ROUTERS
# =====================================

app.include_router(auth_router)
app.include_router(ingredientes_router)
app.include_router(recetas_router)


# =====================================
# ARCHIVOS ESTATICOS DEL FRONTEND
# =====================================

FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)


# =====================================
# RUTA PRINCIPAL - SIRVE EL FRONTEND
# =====================================

@app.get("/")
def inicio():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )


# =====================================
# ESTADO DEL SERVIDOR
# =====================================

@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "aplicacion": "SmartRecipe AI"
    }


# =====================================
# PRUEBA TEMPORAL DE MYSQL
# =====================================

@app.get("/test-db")
def probar_conexion():

    try:
        with engine.connect() as conexion:
            resultado = conexion.execute(
                text("SELECT DATABASE()")
            )

            base_datos = resultado.scalar()

        return {
            "mensaje": "Conexion exitosa con MySQL",
            "base_datos": base_datos
        }

    except SQLAlchemyError:
        return {
            "mensaje": "No se pudo conectar con MySQL"
        }
