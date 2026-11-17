
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioRegistro,
    UsuarioRespuesta
)
from app.services.security import encriptar_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(
    datos: UsuarioRegistro,
    db: Session = Depends(get_db)
):

    # Comprobar si el correo ya está registrado
    usuario_existente = db.query(Usuario).filter(
        Usuario.correo == datos.correo
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    # Proteger contraseña
    password_seguro = encriptar_password(datos.password)

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        password_hash=password_seguro
    )

    # Guardar en MySQL
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario
