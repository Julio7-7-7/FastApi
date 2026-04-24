from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.horario import Horario
from schemas.horario import HorarioCreate, HorarioResponse

router = APIRouter(
    prefix="/horario",
    tags=["Horario"]
)

@router.post("/", response_model=HorarioResponse)
def crear(data: HorarioCreate, db: Session = Depends(get_db)):
    nuevo = Horario(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[HorarioResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Horario).all()

@router.get("/{id}", response_model=HorarioResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="No encontrado")
    return horario

@router.put("/{id}", response_model=HorarioResponse)
def editar(id: int, data: HorarioCreate, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(horario, key, value)
    db.commit()
    db.refresh(horario)
    return horario

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(horario)
    db.commit()
    return {"message": "Eliminado exitosamente"}