from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Programa(Base):
    __tablename__ = "programa"

    id_programa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_tipo_programa = Column(Integer, ForeignKey("tipo_programa.id_tipo_programa"), nullable=False)
    nombre_programa = Column(String, nullable=False)
    vigente = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)