""" 
Maneja el control sobre la información de la vista
y los modelos de bases de datos
"""
from models import db, Usuario, Asistencia

class ControladorUsuarios:
    @staticmethod
    def crear_usuario(status,cargo,numero_t,nombre,apellido_p,apellido_m,work,correo,clave):
        usuario = Usuario()
        usuario.status = status
        usuario.cargo = cargo
        usuario.numero_t = numero_t 
        usuario.nombre = nombre
        usuario.apellido_p = apellido_p
        usuario.apellido_m = apellido_m
        usuario.work = work
        usuario.correo = correo 
        usuario.establecer_clave(clave)
            
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    @staticmethod
    def all_users():
        return Usuario.query.all()
    

class ControladorAsistencia:
    @staticmethod
    def all_asistencias():
        return Asistencia.query.all()
    @staticmethod
    def crear_asistencia(usuario_id, turno,hora_inicio, hora_fin ,fecha_registro, latitud, longitud, tiempo_trabajo):
        asistencia = Asistencia(
            usuario_id=usuario_id,
            turno=turno,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            fecha_registro=fecha_registro,
            latitud=latitud,
            longitud=longitud,
            tiempo_trabajo=tiempo_trabajo,
        )

        db.session.add(asistencia)
        db.session.commit()
        return asistencia