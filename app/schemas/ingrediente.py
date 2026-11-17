
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class IngredienteBase(BaseModel):
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

    @field_validator("nombre", "unidad")
    @classmethod
    def validar_texto(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "Este campo no puede estar vacío"
            )

        return valor


class IngredienteCrear(IngredienteBase):
    pass


class IngredienteActualizar(IngredienteBase):
    pass


class IngredienteRespuesta(IngredienteBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
