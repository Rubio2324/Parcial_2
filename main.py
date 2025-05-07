from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db import engine, crear_db, get_session
from models import Usuario, EstadoUsuario, Tarea, EstadoTarea, TareaCreate
from operations_db import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario,
    usuarios_por_estado,
    usuarios_premium_y_activos,
    crear_tarea,
    obtener_tareas,
    obtener_tarea,
    actualizar_tarea,
    eliminar_tarea
)

app = FastAPI(
    title="API de Gestion de Usuarios y Tareas",
    description="API para gestionar usuarios y sus tareas",
)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API para gestionar Tareas y Usuarios :)"}



@app.on_event("startup")
def startup():
    crear_db()


# Rutas para usuarios
@app.post("/usuarios/", response_model=Usuario, summary="Crear un nuevo usuario")
def crear_nuevo_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    return crear_usuario(session, usuario)


@app.get("/usuarios/", response_model=List[Usuario], summary="Mostrar todos los usuarios")
def listar_usuarios(session: Session = Depends(get_session)):
    return obtener_usuarios(session)


@app.get("/usuarios/{id}", response_model=Usuario, summary="Obtener un usuario por ID")
def ver_usuario(id: int, session: Session = Depends(get_session)):
    return obtener_usuario_por_id(session, id)


@app.put("/usuarios/{id}", response_model=Usuario, summary="Actualizar un usuario")
def actualizar_usuario_endpoint(id: int, datos: Usuario, session: Session = Depends(get_session)):
    return actualizar_usuario(session, id, datos)


@app.delete("/usuarios/{id}", response_model=Usuario, summary="Eliminar un usuario")
def eliminar_usuario_endpoint(id: int, session: Session = Depends(get_session)):
    return eliminar_usuario(session, id)


@app.get("/usuarios/estado/{estado}", response_model=List[Usuario], summary="Filtrar usuarios por estado")
def usuarios_por_estado_endpoint(estado: EstadoUsuario, session: Session = Depends(get_session)):
    return usuarios_por_estado(session, estado)


@app.get("/usuarios/premium/activos", response_model=List[Usuario], summary="Listar usuarios premium y activos")
def premium_activos_endpoint(session: Session = Depends(get_session)):
    return usuarios_premium_y_activos(session)


# Rutas para tareas
@app.post("/tareas/", response_model=Tarea, summary="Crear una nueva tarea")
def crear_nueva_tarea(tarea_data: TareaCreate, session: Session = Depends(get_session)):
    nueva_tarea = Tarea(**tarea_data.dict())
    return crear_tarea(session, nueva_tarea)


@app.get("/tareas/", response_model=List[Tarea], summary="Mostar todas las tareas")
def listar_todas_tareas(session: Session = Depends(get_session)):
    return obtener_tareas(session)


@app.get("/tareas/{tarea_id}", response_model=Tarea, summary="Obtener una tarea por ID")
def obtener_tarea_endpoint(tarea_id: int, session: Session = Depends(get_session)):
    return obtener_tarea(session, tarea_id)


@app.put("/tareas/{tarea_id}", response_model=Tarea, summary="Actualizar una tarea")
def actualizar_tarea_endpoint(tarea_id: int, tarea: TareaCreate, session: Session = Depends(get_session)):
    tarea_actualizada = Tarea(**tarea.dict())
    return actualizar_tarea(session, tarea_id, tarea_actualizada)


@app.delete("/tareas/{tarea_id}", summary="Eliminar una tarea")
def eliminar_tarea_endpoint(tarea_id: int, session: Session = Depends(get_session)):
    return eliminar_tarea(session, tarea_id)

@app.get("/tareas/usuario/{usuario_id}", response_model=List[Tarea], summary="mostrar tareas de un usuario")
def tareas_por_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f" Pailas Usuario con ID {usuario_id} no encontrado")
    tareas = session.exec(select(Tarea).where(Tarea.usuario == usuario_id)).all()
    return tareas


@app.get("/tareas/estado/{estado}", response_model=List[Tarea], summary="Filtrar tareas por estado")
def tareas_por_estado(estado: EstadoTarea, session: Session = Depends(get_session)):
    tareas = session.exec(select(Tarea).where(Tarea.estado == estado)).all()
    return tareas