from fastapi import FastAPI
from database import Base, engine
from routers import tipo_programa

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tipo_programa.router)

@app.get("/")
def root():
    return {"API Posgrado funcionando ✅"}