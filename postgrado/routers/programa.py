from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.programa import Programa
from schemas.programa import ProgramaCreate, ProgramaResponse

router = APIRouter(
    prefix="/programa",
    tags=["Programa"]
)

@router.post("/", response_model=ProgramaResponse)
def crear(data: ProgramaCreate, db: Session = Depends(get_db)):
    nuevo = Programa(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[ProgramaResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Programa).all()

@router.get("/{id}", response_model=ProgramaResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id_programa == id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="No encontrado")
    return programa

@router.put("/{id}", response_model=ProgramaResponse)
def editar(id: int, data: ProgramaCreate, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id_programa == id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(programa, key, value)
    db.commit()
    db.refresh(programa)
    return programa

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id_programa == id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(programa)
    db.commit()
    return {"message": "Eliminado exitosamente"}