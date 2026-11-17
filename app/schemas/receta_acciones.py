
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


# =====================================
# ACTUALIZAR FAVORITA
# =====================================

class FavoritaActualizar(BaseModel):
    favorita: bool


# =====================================
# CALIFICAR UNA RECETA
# =====================================

class CalificacionCrear(BaseModel):
    puntuacion: int = Field(
        ge=1,
        le=5,
        strict=True,
        description="Puntuación entre 1 y 5 estrellas"
    )


# =====================================
# RESPUESTA DE CALIFICACION
# =====================================

class CalificacionRespuesta(BaseModel):
    id: int
    usuario_id: int
    receta_id: int
    puntuacion: int
    fecha_calificacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
