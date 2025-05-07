from sqlmodel import Session, select
from fastapi import HTTPException, status
from models import Usuario, EstadoUsuario, Tarea, EstadoTarea
from datetime import datetime


def crear_usuario(session: Session, usuario: Usuario):
    existente = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    existente2 = session.get(Usuario, usuario.id)
    if existente2:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con ID {usuario.id}"
        )
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe un usuario con el email {usuario.email}")

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def obtener_usuarios(session: Session):
    usuarios = session.exec(select(Usuario).where(Usuario.estado != EstadoUsuario.eliminado)).all()
    if not usuarios:
        return []
    return usuarios


def obtener_usuario_por_id(session: Session, id: int):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {id} no encontrado")
    return usuario


def actualizar_usuario(session: Session, id: int, datos: Usuario):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {id} no encontrado")
    if datos.email != usuario.email:
        existente = session.exec(select(Usuario).where(Usuario.email == datos.email)).first()
        if existente:
            raise HTTPException(status_code=400, detail=f"El email {datos.email} ya está en uso")

    usuario.nombre = datos.nombre
    usuario.email = datos.email
    usuario.premium = datos.premium
    session.commit()
    session.refresh(usuario)
    return usuario


def eliminar_usuario(session: Session, id: int):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {id} no encontrado")

    usuario.estado = EstadoUsuario.eliminado
    session.commit()
    session.refresh(usuario)
    return usuario


def usuarios_por_estado(session: Session, estado: EstadoUsuario):
    usuarios = session.exec(select(Usuario).where(Usuario.estado == estado)).all()
    if not usuarios:
        return []
    return usuarios


def usuarios_premium_y_activos(session: Session):
    usuarios = session.exec(
        select(Usuario).where(Usuario.estado == EstadoUsuario.activo, Usuario.premium == True)
    ).all()
    if not usuarios:
        return []
    return usuarios


def crear_tarea(session: Session, tarea: Tarea):
    if tarea.id is not None:
        existente = session.get(Tarea, tarea.id)
        if existente:
            raise HTTPException(status_code=400, detail=f"Ya existe una tarea con ID {tarea.id}")
    usuario = session.get(Usuario, tarea.usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {tarea.usuario} no encontrado")

    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea


def obtener_tareas(session: Session):
    tareas = session.exec(select(Tarea)).all()
    return tareas


def obtener_tarea(session: Session, tarea_id: int):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {tarea_id} no encontrada")
    return tarea


def actualizar_tarea(session: Session, tarea_id: int, nueva_tarea: Tarea):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {tarea_id} no encontrada")
    if nueva_tarea.usuario != tarea.usuario:
        usuario = session.get(Usuario, nueva_tarea.usuario)
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuario con ID {nueva_tarea.usuario} no encontrado")

    tarea.nombre = nueva_tarea.nombre
    tarea.descripcion = nueva_tarea.descripcion
    tarea.estado = nueva_tarea.estado
    tarea.usuario = nueva_tarea.usuario
    tarea.fecha_modificacion = datetime.utcnow()

    session.commit()
    session.refresh(tarea)
    return tarea


def eliminar_tarea(session: Session, tarea_id: int):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {tarea_id} no encontrada")

    session.delete(tarea)
    session.commit()
    return {"mensaje": f"Tarea con ID {tarea_id} eliminada correctamente"}