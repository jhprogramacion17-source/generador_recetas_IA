
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey
)

from app.models.usuario import Base


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    cantidad = Column(
        Numeric(10, 2),
        nullable=False
    )

    unidad = Column(
        String(30),
        nullable=False
    )
