from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from db import crear_db, get_session
from models import Usuario, EstadoUsuario
from operations_db import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario,
    usuarios_por_estado,
    usuarios_premium_y_activos
)

app = FastAPI()

@app.on_event("startup")
def startup():
    crear_db()

@app.post("/usuarios/")
def crear(usuario: Usuario, session: Session = Depends(get_session)):
    return crear_usuario(session, usuario)

@app.get("/usuarios/")
def listar(session: Session = Depends(get_session)):
    return obtener_usuarios(session)

@app.get("/usuarios/{id}")
def ver(id: int, session: Session = Depends(get_session)):
    usuario = obtener_usuario_por_id(session, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{id}")
def actualizar(id: int, datos: Usuario, session: Session = Depends(get_session)):
    usuario = actualizar_usuario(session, id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/usuarios/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    usuario = eliminar_usuario(session, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/estado/{estado}")
def por_estado(estado: EstadoUsuario, session: Session = Depends(get_session)):
    return usuarios_por_estado(session, estado)

@app.get("/usuarios/premium/activos")
def premium_activos(session: Session = Depends(get_session)):
    return usuarios_premium_y_activos(session)