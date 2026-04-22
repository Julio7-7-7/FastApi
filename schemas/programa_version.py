from pydantic import BaseModel
from datetime import datetime

class ProgramaVersionBase(BaseModel):
    id_programa: int

class ProgramaVersionCreate(ProgramaVersionBase):
    pass

class ProgramaVersionResponse(ProgramaVersionBase):
    id_programa_version: int
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True