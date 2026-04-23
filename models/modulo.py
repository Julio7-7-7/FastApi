from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from database import Base

class Modulo(Base):
    __tablename__ = "modulo"

    id_modulo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_programa_version = Column(Integer, ForeignKey("programa_version.id_programa_version"), nullable=False)
    sigla = Column(String, nullable=False)
    nombre_modulo = Column(String, nullable=False)
    horas_academicas = Column(Integer, nullable=False)
    creditos = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)
    vigente = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)