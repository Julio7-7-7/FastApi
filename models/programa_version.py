from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class ProgramaVersion(Base):
    __tablename__ = "programa_version"

    id_programa_version = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_programa = Column(Integer, ForeignKey("programa.id_programa"), nullable=False)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)