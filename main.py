from fastapi import FastAPI
from database import Base, engine
from routers import tipo_programa, programa, programa_version

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tipo_programa.router)
app.include_router(programa.router)
app.include_router(programa_version.router)

@app.get("/")
def root():
    return {"message": "API Posgrado funcionando ✅"}