
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UsuarioRegistro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: EmailStr

    model_config = ConfigDict(from_attributes=True)
