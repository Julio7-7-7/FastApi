from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class HistorialModulo(Base):
    __tablename__ = "historial_modulo"

    id_historial = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_detalle_programa_modulo = Column(Integer, ForeignKey("detalle_programa_modulo.id_detalle_programa_modulo"), nullable=False)
    estado_anterior = Column(String(20), nullable=False)
    estado_nuevo = Column(String(20), nullable=False)
    motivo = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    detalle_programa_modulo = relationship("DetalleProgramaModulo", back_populates="historial")