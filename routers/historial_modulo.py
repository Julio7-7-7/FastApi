from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.historial_modulo import HistorialModulo
from schemas.historial_modulo import HistorialModuloCreate, HistorialModuloResponse

router = APIRouter(
    prefix="/historial-modulo",
    tags=["Historial Modulo"]
)

@router.post("/", response_model=HistorialModuloResponse, status_code=201)
def crear(data: HistorialModuloCreate, db: Session = Depends(get_db)):
    nuevo = HistorialModulo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[HistorialModuloResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(HistorialModulo).all()

@router.get("/detalle/{id_detalle}", response_model=list[HistorialModuloResponse])
def listar_por_detalle(id_detalle: int, db: Session = Depends(get_db)):
    return db.query(HistorialModulo).filter(
        HistorialModulo.id_detalle_programa_modulo == id_detalle
    ).all()

@router.get("/{id}", response_model=HistorialModuloResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    historial = db.query(HistorialModulo).filter(
        HistorialModulo.id_historial == id
    ).first()
    if not historial:
        raise HTTPException(status_code=404, detail="No encontrado")
    return historial