
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuario import Usuario
from app.models.ingrediente import Ingrediente

from app.schemas.ingrediente import (
    IngredienteCrear,
    IngredienteActualizar,
    IngredienteRespuesta
)

from app.services.jwt_service import obtener_usuario_actual


# Configuración del router
router = APIRouter(
    prefix="/ingredientes",
    tags=["Ingredientes"]
)


# ==========================================
# CREAR INGREDIENTE
# ==========================================

@router.post(
    "/",
    response_model=IngredienteRespuesta,
    status_code=status.HTTP_201_CREATED
)
def crear_ingrediente(
    datos: IngredienteCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):

    nuevo_ingrediente = Ingrediente(
        nombre=datos.nombre,
        cantidad=datos.cantidad,
        unidad=datos.unidad,
        usuario_id=usuario_actual.id
    )

    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)

    return nuevo_ingrediente


# ==========================================
# LISTAR MIS INGREDIENTES
# ==========================================

@router.get(
    "/",
    response_model=list[IngredienteRespuesta]
)
def listar_ingredientes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):

    ingredientes = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.usuario_id == usuario_actual.id
        )
        .order_by(Ingrediente.id)
        .all()
    )

    return ingredientes


# ==========================================
# BUSCAR INGREDIENTE POR ID
# ==========================================

@router.get(
    "/{ingrediente_id}",
    response_model=IngredienteRespuesta
)
def obtener_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):

    ingrediente = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.id == ingrediente_id,
            Ingrediente.usuario_id == usuario_actual.id
        )
        .first()
    )

    if ingrediente is None:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    return ingrediente


# ==========================================
# ACTUALIZAR INGREDIENTE
# ==========================================

@router.put(
    "/{ingrediente_id}",
    response_model=IngredienteRespuesta
)
def actualizar_ingrediente(
    ingrediente_id: int,
    datos: IngredienteActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):

    ingrediente = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.id == ingrediente_id,
            Ingrediente.usuario_id == usuario_actual.id
        )
        .first()
    )

    if ingrediente is None:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    ingrediente.nombre = datos.nombre
    ingrediente.cantidad = datos.cantidad
    ingrediente.unidad = datos.unidad

    db.commit()
    db.refresh(ingrediente)

    return ingrediente


# ==========================================
# ELIMINAR INGREDIENTE
# ==========================================

@router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):

    ingrediente = (
        db.query(Ingrediente)
        .filter(
            Ingrediente.id == ingrediente_id,
            Ingrediente.usuario_id == usuario_actual.id
        )
        .first()
    )

    if ingrediente is None:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    db.delete(ingrediente)
    db.commit()

    return None
