
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioRegistro, UsuarioRespuesta

from app.services.security import (
    encriptar_password,
    verificar_password
)

from app.services.jwt_service import (
    crear_token,
    obtener_usuario_actual
)
from app.services.security import verificar_password
from app.services.jwt_service import crear_token

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


@router.post("/login")
def iniciar_sesion(
    formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(
        Usuario.correo == formulario.username
    ).first()

    # Verificar credenciales
    if not usuario or not verificar_password(
        formulario.password,
        usuario.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generar token de acceso
    token = crear_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/perfil", response_model=UsuarioRespuesta)
def obtener_perfil(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    return usuario_actual
