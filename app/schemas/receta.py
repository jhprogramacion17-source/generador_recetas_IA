
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class IngredienteReceta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(
        min_length=1,
        max_length=100
    )
    cantidad: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    unidad: str = Field(
        min_length=1,
        max_length=30
    )


class RecetaGenerada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(
        min_length=3,
        max_length=150
    )

    ingredientes: list[IngredienteReceta] = Field(
        min_length=1,
        max_length=30
    )

    pasos: list[str] = Field(
        min_length=1,
        max_length=20
    )

    tiempo_estimado: int = Field(
        ge=1,
        le=1440
    )

    dificultad: Literal[
        "Fácil",
        "Media",
        "Difícil"
    ]

    @field_validator("pasos")
    @classmethod
    def validar_pasos(cls, pasos: list[str]):
        pasos_limpios = [
            paso.strip() for paso in pasos
        ]

        if any(not paso for paso in pasos_limpios):
            raise ValueError(
                "Los pasos no pueden estar vacíos"
            )

        return pasos_limpios


class RecetaRespuesta(BaseModel):
    id: int
    usuario_id: int
    nombre: str

    ingredientes_json: list[IngredienteReceta]
    pasos_json: list[str]

    tiempo_estimado: int
    dificultad: str
    favorita: bool
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
