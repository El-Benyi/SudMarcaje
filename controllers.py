""" 
Maneja el control sobre la información de la vista
y los modelos de bases de datos
"""
from models import db, Usuario, Asistencia

class ControladorUsuarios:
    @staticmethod
    def crear_usuario(status,cargo,numero_t,nombre,apellido_p,apellido_m,correo,clave):
        usuario = Usuario()
        usuario.status = status
        usuario.cargo = cargo
        usuario.numero_t = numero_t 
        usuario.nombre = nombre
        usuario.apellido_p = apellido_p
        usuario.apellido_m = apellido_m
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
    def crear_asistencia(user_mail, hora_inicio, hora_termino,fecha_registro, turno):
        if not user_mail:
            print("El correo electrónico es obligatorio.")
            return None

        usuario = Usuario.obtener_por_correo(user_mail)
        if not usuario:
            print(f"No se encontró el usuario con correo: {user_mail}")
            return None 

        # Crear la nueva asistencia
        asistencia = Asistencia()
        asistencia.hora_inicio = hora_inicio
        asistencia.hora_termino = hora_termino
        asistencia.fecha_registro = fecha_registro
        asistencia.turno = turno
        asistencia.usuario_id = usuario.id  

        db.session.add(asistencia)
        db.session.commit()

        return asistencia