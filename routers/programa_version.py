from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.programa_version import ProgramaVersion
from schemas.programa_version import ProgramaVersionCreate, ProgramaVersionResponse

router = APIRouter(
    prefix="/programa-version",
    tags=["Programa Version"]
)

@router.post("/", response_model=ProgramaVersionResponse)
def crear(data: ProgramaVersionCreate, db: Session = Depends(get_db)):
    ultima = db.query(ProgramaVersion).filter(
        ProgramaVersion.id_programa == data.id_programa
    ).count()
    nueva = ProgramaVersion(
        id_programa=data.id_programa,
        version=ultima + 1
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ProgramaVersionResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ProgramaVersion).all()

@router.get("/{id}", response_model=ProgramaVersionResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    pv = db.query(ProgramaVersion).filter(ProgramaVersion.id_programa_version == id).first()
    if not pv:
        raise HTTPException(status_code=404, detail="No encontrado")
    return pv

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    pv = db.query(ProgramaVersion).filter(ProgramaVersion.id_programa_version == id).first()
    if not pv:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(pv)
    db.commit()
    return {"message": "Eliminado exitosamente"}