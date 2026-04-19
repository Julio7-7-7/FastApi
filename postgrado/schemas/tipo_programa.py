from pydantic import BaseModel

class TipoProgramaBase(BaseModel):
    nombre: str

class TipoProgramaCreate(TipoProgramaBase):
    pass

class TipoProgramaResponse(TipoProgramaBase):
    id_tipo_programa: int

    class Config:
        from_attributes = True 