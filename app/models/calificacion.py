
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint
)

from sqlalchemy.sql import func

from app.models.usuario import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "receta_id",
            name="uq_usuario_receta"
        ),
        CheckConstraint(
            "puntuacion BETWEEN 1 AND 5",
            name="chk_calificacion_valida"
        )
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    receta_id = Column(
        Integer,
        ForeignKey(
            "recetas.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    puntuacion = Column(
        Integer,
        nullable=False
    )

    fecha_calificacion = Column(
        DateTime,
        server_default=func.now()
    )
