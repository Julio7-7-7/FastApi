from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum

class EstadoEnum(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class TipoProgramaBase(BaseModel):
    nombre: str
    estado: EstadoEnum = EstadoEnum.activo

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if len(v.strip()) > 100:
            raise ValueError("El nombre no puede superar 100 caracteres")
        return v.strip().title()

class TipoProgramaCreate(TipoProgramaBase):
    pass

class TipoProgramaUpdate(BaseModel):
    nombre: str | None = None
    estado: EstadoEnum | None = None

class TipoProgramaResponse(TipoProgramaBase):
    id_tipo_programa: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True