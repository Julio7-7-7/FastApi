from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from database import get_db
from models.programa import Programa
from models.programa_version import ProgramaVersion
from schemas.programa_version import ProgramaVersionCreate, ProgramaVersionUpdate, ProgramaVersionResponse

router = APIRouter(
    prefix="/programas-version",
    tags=["Programas Version"]
)

@router.post("/", response_model=ProgramaVersionResponse, status_code=201)
def crear(data: ProgramaVersionCreate, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id_programa == data.id_programa).first()
    if not programa:
        raise HTTPException(status_code=404, detail="El programa especificado no existe")

    ultima = db.query(ProgramaVersion).filter(
        ProgramaVersion.id_programa == data.id_programa
    ).count()

    try:
        nueva = ProgramaVersion(
            **data.model_dump(),
            version=ultima + 1
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto: la versión ya fue creada por otra solicitud. Intente nuevamente."
        )

@router.get("/", response_model=list[ProgramaVersionResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ProgramaVersion).options(joinedload(ProgramaVersion.programa)).all()

@router.get("/{id}", response_model=ProgramaVersionResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    pv = db.query(ProgramaVersion).options(joinedload(ProgramaVersion.programa)).filter(
        ProgramaVersion.id_programa_version == id
    ).first()
    if not pv:
        raise HTTPException(status_code=404, detail="No encontrado")
    return pv

@router.patch("/{id}", response_model=ProgramaVersionResponse)
def editar(id: int, data: ProgramaVersionUpdate, db: Session = Depends(get_db)):
    pv = db.query(ProgramaVersion).options(joinedload(ProgramaVersion.programa)).filter(
        ProgramaVersion.id_programa_version == id
    ).first()
    if not pv:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pv, key, value)
    db.commit()
    db.refresh(pv)
    return pv