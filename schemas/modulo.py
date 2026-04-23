from pydantic import BaseModel
from datetime import datetime

class ModuloBase(BaseModel):
    id_programa_version: int
    sigla: str
    nombre_modulo: str
    horas_academicas: int
    creditos: int
    descripcion: str | None = None
    vigente: bool = True

class ModuloCreate(ModuloBase):
    pass

class ModuloResponse(ModuloBase):
    id_modulo: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True