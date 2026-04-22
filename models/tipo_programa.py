from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class TipoPrograma(Base):
    __tablename__ = "tipo_programa"

    id_tipo_programa = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)