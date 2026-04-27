from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.horario import Horario
from models.detalle_programa_modulo import DetalleProgramaModulo
from schemas.horario import HorarioCreate, HorarioUpdate, HorarioResponse

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)

def verificar_solapamiento(db, id_detalle, dia, hora_ini, hora_fin, excluir_id=None):
    # verificar solapamiento en el mismo módulo
    query = db.query(Horario).filter(
        Horario.id_detalle_programa_modulo == id_detalle,
        Horario.dia == dia,
        Horario.hora_ini < hora_fin,
        Horario.hora_fin > hora_ini
    )
    if excluir_id:
        query = query.filter(Horario.id_horario != excluir_id)
    if query.first():
        raise HTTPException(status_code=400, detail="El horario se solapa con otro horario existente en este módulo")

def verificar_docente(db: Session, id_detalle: int, dia: str, hora_ini, hora_fin, excluir_id: int = None):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id_detalle
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de módulo no encontrado")

    choque = db.query(Horario).join(
        DetalleProgramaModulo,
        Horario.id_detalle_programa_modulo == DetalleProgramaModulo.id_detalle_programa_modulo
    ).filter(
        DetalleProgramaModulo.id_docente == detalle.id_docente,
        DetalleProgramaModulo.estado.in_(["programado", "en_curso"]),
        Horario.dia == dia,
        Horario.hora_ini < hora_fin,
        Horario.hora_fin > hora_ini
    )

    if excluir_id:
        choque = choque.filter(Horario.id_horario != excluir_id)

    conflicto = choque.first()
    if conflicto:
        raise HTTPException(
            status_code=400,
            detail=f"Conflicto de agenda: el docente ya tiene clase el {dia} de {conflicto.hora_ini} a {conflicto.hora_fin}"
        )

@router.post("/", response_model=HorarioResponse, status_code=201)
def crear(data: HorarioCreate, db: Session = Depends(get_db)):
    verificar_solapamiento(db, data.id_detalle_programa_modulo, data.dia, data.hora_ini, data.hora_fin)
    verificar_docente(db, data.id_detalle_programa_modulo, data.dia, data.hora_ini, data.hora_fin)
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

@router.patch("/{id}", response_model=HorarioResponse)
def editar(id: int, data: HorarioUpdate, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="No encontrado")
    hora_ini = data.hora_ini or horario.hora_ini
    hora_fin = data.hora_fin or horario.hora_fin
    dia = data.dia or horario.dia
    verificar_solapamiento(db, horario.id_detalle_programa_modulo, dia, hora_ini, hora_fin, excluir_id=id)
    verificar_docente(db, horario.id_detalle_programa_modulo, dia, hora_ini, hora_fin, excluir_id=id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(horario, key, value)
    db.commit()
    db.refresh(horario)
    return horario

@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(horario)
    db.commit()