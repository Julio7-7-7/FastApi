from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class DetalleProgramaModulo(Base):
    __tablename__ = "detalle_programa_modulo"

    id_detalle_programa_modulo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_programa_version_edicion = Column(Integer, ForeignKey("programa_version_edicion.id_programa_version_edicion"), nullable=False)
    id_modulo = Column(Integer, ForeignKey("modulos.id_modulo"), nullable=False)
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"), nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String, nullable=False, default="programado")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)