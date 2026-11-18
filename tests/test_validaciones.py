
import json

import pytest

from pydantic import ValidationError

from app.schemas.ingrediente import (
    IngredienteCrear
)

from app.schemas.receta import (
    RecetaGenerada
)

from app.services.llm_service import (
    ErrorLLM,
    construir_prompt,
    parsear_receta
)


# =====================================
# DATOS DE PRUEBA
# =====================================

@pytest.fixture
def inventario():
    return [
        {
            "nombre": "Arroz",
            "cantidad": "500",
            "unidad": "gramos"
        },
        {
            "nombre": "Pollo",
            "cantidad": "300",
            "unidad": "gramos"
        }
    ]


@pytest.fixture
def receta_json():
    return json.dumps({
        "nombre": "Arroz con pollo",
        "ingredientes": [
            {
                "nombre": "Arroz",
                "cantidad": 200,
                "unidad": "gramos"
            },
            {
                "nombre": "Pollo",
                "cantidad": 250,
                "unidad": "gramos"
            }
        ],
        "pasos": [
            "Cocinar el arroz.",
            "Cocinar completamente el pollo.",
            "Mezclar y servir."
        ],
        "tiempo_estimado": 40,
        "dificultad": "Fácil"
    })


# =====================================
# PRUEBA 1: INGREDIENTE VALIDO
# =====================================

def test_crear_ingrediente_valido():
    ingrediente = IngredienteCrear(
        nombre="Arroz",
        cantidad=500,
        unidad="gramos"
    )

    assert ingrediente.nombre == "Arroz"
    assert ingrediente.cantidad == 500


# =====================================
# PRUEBA 2: CANTIDAD NEGATIVA
# =====================================

def test_rechazar_cantidad_negativa():
    with pytest.raises(ValidationError):
        IngredienteCrear(
            nombre="Arroz",
            cantidad=-10,
            unidad="gramos"
        )


# =====================================
# PRUEBA 3: NOMBRE VACIO
# =====================================

def test_rechazar_nombre_vacio():
    with pytest.raises(ValidationError):
        IngredienteCrear(
            nombre="   ",
            cantidad=100,
            unidad="gramos"
        )


# =====================================
# PRUEBA 4: GENERACION DEL PROMPT
# =====================================

def test_prompt_contiene_ingredientes(
    inventario
):
    prompt = construir_prompt(inventario)

    assert "Arroz" in prompt
    assert "Pollo" in prompt
    assert "500" in prompt
    assert "300" in prompt


# =====================================
# PRUEBA 5: PROMPT CON RESTRICCIONES
# =====================================

def test_prompt_incluye_restricciones(
    inventario
):
    prompt = construir_prompt(inventario)

    assert "ingredientes" in prompt.lower()
    assert "cantidades" in prompt.lower()


# =====================================
# PRUEBA 6: JSON VALIDO
# =====================================

def test_parsear_receta_valida(receta_json):
    receta = parsear_receta(receta_json)

    assert isinstance(
        receta,
        RecetaGenerada
    )

    assert receta.nombre == "Arroz con pollo"
    assert receta.tiempo_estimado == 40
    assert len(receta.ingredientes) == 2


# =====================================
# PRUEBA 7: JSON MAL FORMADO
# =====================================

def test_rechazar_json_invalido():
    contenido = "{esto no es JSON valido}"

    with pytest.raises(ErrorLLM):
        parsear_receta(contenido)


# =====================================
# PRUEBA 8: RECETA SIN PASOS
# =====================================

def test_rechazar_receta_sin_pasos(
    receta_json
):
    datos = json.loads(receta_json)
    datos["pasos"] = []

    with pytest.raises(ErrorLLM):
        parsear_receta(
            json.dumps(datos)
        )


# =====================================
# PRUEBA 9: DIFICULTAD INVALIDA
# =====================================

def test_rechazar_dificultad_invalida(
    receta_json
):
    datos = json.loads(receta_json)
    datos["dificultad"] = "Imposible"

    with pytest.raises(ErrorLLM):
        parsear_receta(
            json.dumps(datos)
        )
