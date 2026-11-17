
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    JSON,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.models.usuario import Base


class Receta(Base):
    __tablename__ = "recetas"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = Column(
        String(150),
        nullable=False
    )

    ingredientes_json = Column(
        JSON,
        nullable=False
    )

    pasos_json = Column(
        JSON,
        nullable=False
    )

    tiempo_estimado = Column(
        Integer,
        nullable=False
    )

    dificultad = Column(
        String(20),
        nullable=False
    )

    favorita = Column(
        Boolean,
        nullable=False,
        default=False
    )

    fecha_creacion = Column(
        DateTime,
        server_default=func.now()
    )
