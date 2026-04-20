from sqlalchemy import Column, Integer, String
from database import Base

class TipoPrograma(Base):
    __tablename__ = "tipo_programa"

    id_tipo_programa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
