
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError
)
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuario import Usuario
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta
from app.models.calificacion import Calificacion

from app.schemas.receta import RecetaRespuesta

from app.schemas.receta_acciones import (
    FavoritaActualizar,
    CalificacionCrear,
    CalificacionRespuesta
)

from app.services.jwt_service import (
    obtener_usuario_actual
)

from app.services.llm_service import (
    ErrorLLM,
    generar_receta_ia
)


# =====================================
# CONFIGURACION DEL ROUTER
# =====================================

router = APIRouter(
    prefix="/recetas",
    tags=["Recetas con IA"]
)


# =====================================
# FUNCION INTERNA DE BUSQUEDA
# =====================================

def buscar_receta_usuario(
    receta_id: int,
    usuario_id: int,
    db: Session
) -> Receta:

    receta = (
        db.query(Receta)
        .filter(
            Receta.id == receta_id,
            Receta.usuario_id == usuario_id
        )
        .first()
    )

    if receta is None:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )

    return receta


# =====================================
# GENERAR RECETA CON INTELIGENCIA ARTIFICIAL
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

    # Obtener inventario personal
    ingredientes = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.usuario_id == usuario_actual.id
        )
        .order_by(Ingrediente.id)
        .all()
    )

    if not ingredientes:
        raise HTTPException(
            status_code=400,
            detail=(
                "Debes registrar ingredientes "
                "antes de generar una receta"
            )
        )

    # Preparar ingredientes para OpenRouter
    inventario = [
        {
            "nombre": ingrediente.nombre,
            "cantidad": str(ingrediente.cantidad),
            "unidad": ingrediente.unidad
        }
        for ingrediente in ingredientes
    ]

    # Generar receta utilizando el servicio interno
    try:
        receta_ia = await generar_receta_ia(
            inventario
        )

    except ErrorLLM as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        ) from error

    # Construir objeto de receta
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

    # Guardar en MySQL
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


# =====================================
# HISTORIAL DE RECETAS
# =====================================

@router.get(
    "/",
    response_model=list[RecetaRespuesta]
)
def listar_recetas(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    recetas = (
        db.query(Receta)
        .filter(
            Receta.usuario_id == usuario_actual.id
        )
        .order_by(Receta.id.desc())
        .all()
    )

    return recetas


# =====================================
# LISTAR RECETAS FAVORITAS
# =====================================

@router.get(
    "/favoritas",
    response_model=list[RecetaRespuesta]
)
def listar_favoritas(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    favoritas = (
        db.query(Receta)
        .filter(
            Receta.usuario_id == usuario_actual.id,
            Receta.favorita.is_(True)
        )
        .order_by(Receta.id.desc())
        .all()
    )

    return favoritas


# =====================================
# CONSULTAR UNA RECETA POR ID
# =====================================

@router.get(
    "/{receta_id}",
    response_model=RecetaRespuesta
)
def obtener_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    return buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )


# =====================================
# AGREGAR O QUITAR DE FAVORITAS
# =====================================

@router.patch(
    "/{receta_id}/favorita",
    response_model=RecetaRespuesta
)
def actualizar_favorita(
    receta_id: int,
    datos: FavoritaActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    receta = buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )

    receta.favorita = datos.favorita

    try:
        db.commit()
        db.refresh(receta)

    except SQLAlchemyError as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la favorita"
        ) from error

    return receta


# =====================================
# CALIFICAR RECETA
# =====================================

@router.post(
    "/{receta_id}/calificaciones",
    response_model=CalificacionRespuesta,
    status_code=status.HTTP_201_CREATED
)
def calificar_receta(
    receta_id: int,
    datos: CalificacionCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    # Verificar que la receta pertenece al usuario
    buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )

    # Comprobar si ya existe una calificacion
    existente = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario_actual.id
        )
        .first()
    )

    if existente is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Ya calificaste esta receta. "
                "Utiliza PUT para cambiar la puntuación"
            )
        )

    nueva_calificacion = Calificacion(
        usuario_id=usuario_actual.id,
        receta_id=receta_id,
        puntuacion=datos.puntuacion
    )

    try:
        db.add(nueva_calificacion)
        db.commit()
        db.refresh(nueva_calificacion)

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Esta receta ya tiene una calificación"
        ) from error

    except SQLAlchemyError as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar la calificación"
        ) from error

    return nueva_calificacion


# =====================================
# CAMBIAR CALIFICACION
# =====================================

@router.put(
    "/{receta_id}/calificaciones",
    response_model=CalificacionRespuesta
)
def actualizar_calificacion(
    receta_id: int,
    datos: CalificacionCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )

    calificacion = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario_actual.id
        )
        .first()
    )

    if calificacion is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No has calificado esta receta. "
                "Utiliza POST para crear la calificación"
            )
        )

    calificacion.puntuacion = datos.puntuacion

    try:
        db.commit()
        db.refresh(calificacion)

    except SQLAlchemyError as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la calificación"
        ) from error

    return calificacion


# =====================================
# CONSULTAR MI CALIFICACION
# =====================================

@router.get(
    "/{receta_id}/calificacion",
    response_model=CalificacionRespuesta
)
def consultar_calificacion(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )

    calificacion = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario_actual.id
        )
        .first()
    )

    if calificacion is None:
        raise HTTPException(
            status_code=404,
            detail="Esta receta todavía no tiene calificación"
        )

    return calificacion


# =====================================
# ELIMINAR RECETA DEL HISTORIAL
# =====================================

@router.delete(
    "/{receta_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        obtener_usuario_actual
    )
):

    receta = buscar_receta_usuario(
        receta_id,
        usuario_actual.id,
        db
    )

    try:
        db.delete(receta)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar la receta"
        ) from error

    return None
