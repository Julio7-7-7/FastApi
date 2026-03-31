from fastapi import FastAPI

app = FastAPI()

usuarios = ["Ana","Luis","Pedro"]

@app.get("/")
def inicio():
    return {"mensaje":"Bienvenido"}

@app.get("/usuarios")
def listar_usuarios():
    return usuarios

@app.get("/usuarios/{id}")
def obtener_usuario(id:int):
    return usuarios[id]

@app.post("/usuarios")
def crear_usuario(nombre:str):
    usuarios.append(nombre)
    return {"mensaje":"usuario agregado"}
    
@app.delete("/usuarios/{id}")
def eliminar_usuario(id:int):
    usuarios.pop(id)
    return {"mensaje":"usuario eliminado"}

@app.get("/usuarios/{id}")
def devolver(id:int):
    return usuarios[id];