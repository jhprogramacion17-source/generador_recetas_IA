
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.routers.auth import router as auth_router

# Creamos nuestra aplicación
app = FastAPI(
    title="SmartRecipe AI",
    description="API para generar recetas con inteligencia artificial",
    version="1.0.0"
    
)
app.include_router(auth_router)

# Ruta principal
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a SmartRecipe AI",
        "estado": "Servidor funcionando correctamente"
    }

# Ruta para comprobar el estado de la API
@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "aplicacion": "SmartRecipe AI"
    }


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
