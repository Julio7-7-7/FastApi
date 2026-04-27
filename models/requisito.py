from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Requisito(Base):
    __tablename__ = "requisito"

    id_requisito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_modalidad_academica = Column(Integer, ForeignKey("modalidades_academicas.id_modalidad_academica"), nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    obligatorio = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    modalidad_academica = relationship("ModalidadAcademica", back_populates="requisitos")
