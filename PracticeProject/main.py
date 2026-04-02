#importamos la libreria FastAPI
from fastapi import FastAPI,HTTPException

#importamos pydantic para crear modelos de datos
from pydantic import BaseModel

app=FastAPI()

class Usuario(BaseModel):
  id: int
  nombre: str
  apellido: str
  edad: int

usuarios=[]

@app.get("/")
def saludar():
  return {"message":"Hola Mundo"}

@app.get("/login")
def login():
  return("Ingrese su usuario y contraseña")

@app.post("/usuario")
def crear_usuario(usuario: Usuario):
  nuevoUsuario = Usuario(
    id= len(usuarios) + 1,
    nombre=usuario.nombre,
    apellido=usuario.apellido,
    edad=usuario.edad
  )
  usuarios.append(nuevoUsuario)
  return ("Usuario creado exitosamente")

@app.get("/usuarios")
def obtener_usuarios():
  return usuarios

@app.get("/usuario/{id}")
def obtener_usuario(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
