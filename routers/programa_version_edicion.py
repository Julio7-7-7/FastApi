from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.programa_version_edicion import ProgramaVersionEdicion
from models.programa_version import ProgramaVersion
from models.programa import Programa
from models.tipo_programa import TipoPrograma
from schemas.programa_version_edicion import ProgramaVersionEdicionCreate, ProgramaVersionEdicionUpdate, ProgramaVersionEdicionResponse

router = APIRouter(
    prefix="/programa-version-edicion",
    tags=["Programa Version Edicion"]
)

def calcular_gestion():
    ahora = datetime.now()
    mitad = 1 if ahora.month <= 6 else 2
    return f"{mitad}-{ahora.year}"

def validar_cupo(data, db):
    pv = db.query(ProgramaVersion).filter(
        ProgramaVersion.id_programa_version == data.id_programa_version
    ).first()
    if not pv:
        raise HTTPException(status_code=404, detail="Versión de programa no encontrada")
    programa = db.query(Programa).filter(Programa.id_programa == pv.id_programa).first()
    tipo = db.query(TipoPrograma).filter(TipoPrograma.id_tipo_programa == programa.id_tipo_programa).first()
    if tipo.cupo_minimo and data.cupo_maximo:
        if data.cupo_maximo < tipo.cupo_minimo:
            raise HTTPException(
                status_code=400,
                detail=f"El cupo máximo ({data.cupo_maximo}) no puede ser menor al cupo mínimo del tipo de programa ({tipo.cupo_minimo})"
            )

@router.post("/", response_model=ProgramaVersionEdicionResponse, status_code=201)
def crear(data: ProgramaVersionEdicionCreate, db: Session = Depends(get_db)):
    validar_cupo(data, db)
    ultima = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version == data.id_programa_version
    ).count()
    gestion = data.gestion if data.gestion else calcular_gestion()
    data_dict = data.model_dump(exclude={"gestion"})
    nueva = ProgramaVersionEdicion(
        **data_dict,
        edicion=ultima + 1,
        gestion=gestion
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ProgramaVersionEdicionResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ProgramaVersionEdicion).all()

@router.get("/{id}", response_model=ProgramaVersionEdicionResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    return pve

@router.patch("/{id}", response_model=ProgramaVersionEdicionResponse)
def editar(id: int, data: ProgramaVersionEdicionUpdate, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    if data.cupo_maximo:
        validar_cupo(data, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pve, key, value)
    db.commit()
    db.refresh(pve)
    return pve

@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(pve)
    db.commit()