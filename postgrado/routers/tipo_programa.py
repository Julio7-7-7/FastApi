from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.tipo_programa import TipoPrograma
from schemas.tipo_programa import TipoProgramaCreate, TipoProgramaResponse

router = APIRouter(
    prefix="/tipo-programa",
    tags=["Tipo Programa"]
)

@router.post("/", response_model=TipoProgramaResponse)
def crear(data: TipoProgramaCreate, db: Session = Depends(get_db)):
    nuevo = TipoPrograma(nombre=data.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[TipoProgramaResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(TipoPrograma).all()

@router.get("/{id}", response_model=TipoProgramaResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    tipo = db.query(TipoPrograma).filter(TipoPrograma.id_tipo_programa == id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="No encontrado")
    return tipo

@router.put("/{id}", response_model=TipoProgramaResponse)
def editar(id: int, data: TipoProgramaCreate, db: Session = Depends(get_db)):
    tipo = db.query(TipoPrograma).filter(TipoPrograma.id_tipo_programa == id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="No encontrado")
    tipo.nombre = data.nombre
    db.commit()
    db.refresh(tipo)
    return tipo

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    tipo = db.query(TipoPrograma).filter(TipoPrograma.id_tipo_programa == id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(tipo)
    db.commit()
    return {"message": "Eliminado exitosamente"}