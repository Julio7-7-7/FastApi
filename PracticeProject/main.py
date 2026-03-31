#importamos la libreria FastAPI
from fastapi import FastAPI

#importamos pydantic para crear modelos de datos
from pydantic import BaseModel

app=FastAPI()

class Usuario(BaseModel):
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
  usuarios.append(usuario)
  return {"message":"Usuario creado exitosamente"}

@app.get("/usuarios")
def obtener_usuarios():
  return usuarios



