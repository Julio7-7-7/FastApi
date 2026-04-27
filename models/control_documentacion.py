from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class ControlDocumentacion(Base):
    __tablename__ = "control_documentacion"

    id_control_documentacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_detalle_programa_alumno = Column(Integer, ForeignKey("detalle_programa_alumno.id_detalle_programa_alumno"), nullable=False)
    id_requisito = Column(Integer, ForeignKey("requisitos.id_requisito"), nullable=False)
    entregado = Column(Boolean, default=False, nullable=False)
    fecha_entrega = Column(Date, nullable=True)
    observaciones = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    requisito = relationship("Requisito", back_populates="control_documentacion")
