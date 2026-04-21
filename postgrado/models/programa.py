from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Programa(Base):
    __tablename__ = "programa"

    id_programa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_tipo_programa = Column(Integer, ForeignKey("tipo_programa.id_tipo_programa"), nullable=False)
    nombre_programa = Column(String, nullable=False)
    vigente = Column(Boolean, default=True, nullable=False)