from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class DetalleProgramaAlumno(Base):
    __tablename__ = "detalle_programa_alumno"

    id_detalle_programa_alumno = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_programa_version_edicion = Column(Integer, ForeignKey("programa_version_edicion.id_programa_version_edicion"), nullable=False)
    id_alumno = Column(Integer, ForeignKey("alumno.id_alumno"), nullable=False)
    id_modalidad_academica = Column(Integer, ForeignKey("modalidades_academicas.id_modalidad_academica"), nullable=False)
    descuento = Column(Float, nullable=False, default=0.0)
    estado = Column(String, nullable=False, default="postulante")
    fecha_inscripcion = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    modalidad_academica = relationship("ModalidadAcademica", back_populates="detalles_alumno")