from pydantic import BaseModel

class ProgramaBase(BaseModel):
    id_tipo_programa: int
    nombre_programa: str
    vigente: bool = True

class ProgramaCreate(ProgramaBase):
    pass

class ProgramaResponse(ProgramaBase):
    id_programa: int

    class Config:
        from_attributes = True