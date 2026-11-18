
import pytest

from fastapi.testclient import TestClient

from app.main import app


# =====================================
# CLIENTE DE PRUEBAS
# =====================================

@pytest.fixture
def cliente():
    with TestClient(app) as test_client:
        yield test_client


# =====================================
# PRUEBA 1: ESTADO DEL SERVIDOR
# =====================================

def test_health(cliente):
    respuesta = cliente.get("/health")

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert datos["status"] == "ok"
    assert datos["aplicacion"] == "SmartRecipe AI"


# =====================================
# PRUEBA 2: PAGINA PRINCIPAL HTML
# =====================================

def test_inicio(cliente):
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200

    # La ruta principal ahora devuelve HTML
    content_type = respuesta.headers.get(
        "content-type",
        ""
    )

    assert "text/html" in content_type

    # Verificar que se recibe el documento HTML
    contenido = respuesta.text.lower()

    assert "<!doctype html" in contenido
    assert "</html>" in contenido

    # Verificar el nombre de la aplicacion
    assert "smartrecipe" in contenido


# =====================================
# PRUEBA 3: INGREDIENTES SIN JWT
# =====================================

def test_ingredientes_sin_token(cliente):
    respuesta = cliente.get("/ingredientes/")

    assert respuesta.status_code == 401


# =====================================
# PRUEBA 4: GENERACION SIN JWT
# =====================================

def test_generar_receta_sin_token(cliente):
    respuesta = cliente.post("/recetas/generar")

    assert respuesta.status_code == 401


# =====================================
# PRUEBA 5: PERFIL SIN JWT
# =====================================

def test_perfil_sin_token(cliente):
    respuesta = cliente.get("/auth/perfil")

    assert respuesta.status_code == 401
