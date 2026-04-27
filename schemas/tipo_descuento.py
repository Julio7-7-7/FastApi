from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum

class EstadoTipoDescuentoEnum(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class TipoDescuentoBase(BaseModel):
    nombre: str
    porcentaje: float
    descripcion: str | None = None
    requiere_documento: bool = False
    id_requisito_extra: int | None = None
    estado: EstadoTipoDescuentoEnum = EstadoTipoDescuentoEnum.activo

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return v.strip().title()

    @field_validator("porcentaje")
    @classmethod
    def validar_porcentaje(cls, v):
        if v <= 0 or v > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        return v

class TipoDescuentoCreate(TipoDescuentoBase):
    pass

class TipoDescuentoUpdate(BaseModel):
    nombre: str | None = None
    porcentaje: float | None = None
    descripcion: str | None = None
    requiere_documento: bool | None = None
    id_requisito_extra: int | None = None
    estado: EstadoTipoDescuentoEnum | None = None

class TipoDescuentoResponse(TipoDescuentoBase):
    id_tipo_descuento: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True