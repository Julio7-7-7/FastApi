from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.control_documentacion import ControlDocumentacion
from schemas.control_documentacion import ControlDocumentacionCreate, ControlDocumentacionResponse

router = APIRouter(
    prefix="/control-documentacion",
    tags=["Control Documentacion"]
)

@router.post("/", response_model=ControlDocumentacionResponse)
def crear(data: ControlDocumentacionCreate, db: Session = Depends(get_db)):
    nuevo = ControlDocumentacion(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[ControlDocumentacionResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ControlDocumentacion).all()

@router.get("/{id}", response_model=ControlDocumentacionResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    control = db.query(ControlDocumentacion).filter(
        ControlDocumentacion.id_control_documentacion == id
    ).first()
    if not control:
        raise HTTPException(status_code=404, detail="No encontrado")
    return control

@router.put("/{id}", response_model=ControlDocumentacionResponse)
def editar(id: int, data: ControlDocumentacionCreate, db: Session = Depends(get_db)):
    control = db.query(ControlDocumentacion).filter(
        ControlDocumentacion.id_control_documentacion == id
    ).first()
    if not control:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(control, key, value)
    db.commit()
    db.refresh(control)
    return control

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    control = db.query(ControlDocumentacion).filter(
        ControlDocumentacion.id_control_documentacion == id
    ).first()
    if not control:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(control)
    db.commit()
    return {"message": "Eliminado exitosamente"}