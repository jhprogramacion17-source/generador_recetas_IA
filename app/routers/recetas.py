
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuario import Usuario
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta

from app.schemas.receta import RecetaRespuesta

from app.services.jwt_service import (
    obtener_usuario_actual
)

from app.services.llm_service import (
    ErrorLLM,
    generar_receta_ia
)


# =====================================
# ROUTER DE RECETAS
# =====================================

router = APIRouter(
    prefix="/recetas",
    tags=["Recetas con IA"]
)


# =====================================
# GENERAR Y GUARDAR UNA RECETA
# =====================================

@router.post(
    "/generar",
    response_model=RecetaRespuesta,
    status_code=status.HTTP_201_CREATED
)
async def generar_receta(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    # Consultar el inventario del usuario
    ingredientes = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.usuario_id == usuario_actual.id
        )
        .order_by(Ingrediente.id)
        .all()
    )

    # Validar que el inventario no esté vacío
    if not ingredientes:
        raise HTTPException(
            status_code=400,
            detail=(
                "Debes registrar ingredientes "
                "antes de generar una receta"
            )
        )

    # Preparar inventario para OpenRouter
    inventario = [
        {
            "nombre": ingrediente.nombre,
            "cantidad": str(ingrediente.cantidad),
            "unidad": ingrediente.unidad
        }
        for ingrediente in ingredientes
    ]

    # Solicitar la receta a la IA
    try:
        receta_ia = await generar_receta_ia(
            inventario
        )

    except ErrorLLM as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        ) from error

    # Preparar la receta para MySQL
    nueva_receta = Receta(
        usuario_id=usuario_actual.id,
        nombre=receta_ia.nombre,

        ingredientes_json=[
            ingrediente.model_dump(mode="json")
            for ingrediente in receta_ia.ingredientes
        ],

        pasos_json=receta_ia.pasos,

        tiempo_estimado=receta_ia.tiempo_estimado,
        dificultad=receta_ia.dificultad,
        favorita=False
    )

    # Guardar en la base de datos
    try:
        db.add(nueva_receta)
        db.commit()
        db.refresh(nueva_receta)

    except SQLAlchemyError as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar la receta"
        ) from error

    return nueva_receta
