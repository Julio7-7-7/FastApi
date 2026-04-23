from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.modulo import Modulo
from schemas.modulo import ModuloCreate, ModuloResponse

router = APIRouter(
    prefix="/modulo",
    tags=["Modulo"]
)

@router.post("/", response_model=ModuloResponse)
def crear(data: ModuloCreate, db: Session = Depends(get_db)):
    nuevo = Modulo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[ModuloResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Modulo).all()

@router.get("/{id}", response_model=ModuloResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    modulo = db.query(Modulo).filter(Modulo.id_modulo == id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="No encontrado")
    return modulo

@router.put("/{id}", response_model=ModuloResponse)
def editar(id: int, data: ModuloCreate, db: Session = Depends(get_db)):
    modulo = db.query(Modulo).filter(Modulo.id_modulo == id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(modulo, key, value)
    db.commit()
    db.refresh(modulo)
    return modulo

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    modulo = db.query(Modulo).filter(Modulo.id_modulo == id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(modulo)
    db.commit()
    return {"message": "Eliminado exitosamente"}