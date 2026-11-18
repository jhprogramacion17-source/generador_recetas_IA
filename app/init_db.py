from app.database import engine
from app.models import calificacion, ingrediente, receta
from app.models.usuario import Base


if __name__ == "__main__":
    # Los módulos de modelos registran las tablas en Base.metadata.
    Base.metadata.create_all(bind=engine)
