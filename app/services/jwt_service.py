
import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.database import get_db
from app.models.usuario import Usuario
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
EXPIRATION_MINUTES = int(
    os.getenv("JWT_EXPIRATION_MINUTES", "30")
)


def crear_token(usuario_id: int):
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=EXPIRATION_MINUTES
    )

    datos = {
        "sub": str(usuario_id),
        "exp": expiracion
    }

    token = jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = datos.get("sub")

        if usuario_id is None:
            raise error_credenciales

        usuario_id = int(usuario_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise error_credenciales

    usuario = db.get(Usuario, usuario_id)

    if usuario is None:
        raise error_credenciales

    return usuario

