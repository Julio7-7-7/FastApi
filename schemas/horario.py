from pydantic import BaseModel
from datetime import datetime, time
from enum import Enum

class DiaEnum(str, Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"

class HorarioBase(BaseModel):
    id_detalle_programa_modulo: int
    dia: DiaEnum
    hora_ini: time
    hora_fin: time

class HorarioCreate(HorarioBase):
    pass

class HorarioResponse(HorarioBase):
    id_horario: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True