"""
    Archivo de modelos de bases de datos
"""
from app import db
from sqlalchemy import func
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash 

#Modelos de bases de datos
class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido_p = db.Column(db.String(255), nullable=True)
    apellido_m = db.Column(db.String(255), nullable=True)
    numero_t  = db.Column(db.String(15), nullable=True)
    work      = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), nullable=True, unique=True)
    clave = db.Column(db.String(255), nullable=True)
    
    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)
    
    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return(all_items_list)     
    @staticmethod 
    def obtener_por_correo(correo):
        usuario = Usuario.query.filter_by(correo=correo).first()
        print(f"Consultando por el usuario {usuario} en db")
        return(usuario)
    @staticmethod
    def obtener_por_id(id):
        print(f"Consultando por el usuario con id{id} en db")
        return Usuario.query.get(id)

    #Relaciones 
    asistencias     = db.relationship("Asistencia", back_populates="usuario")


class Asistencia(db.Model):
    __tablename__   = "asistencia"
    id              = db.Column(db.Integer, primary_key = True)
    fecha_registro  = db.Column(db.Date(), nullable=False)
    hora_registro   = db.Column(db.Time(), nullable=False, default=func.now())
    turno           = db.Column(db.String(255), nullable=False)
    hora_inicio     = db.Column(db.Time(), nullable=False)  
    hora_fin        = db.Column(db.Time(), nullable=True)  
    latitud         = db.Column(db.Float, nullable=True)  
    longitud        = db.Column(db.Float, nullable=True) 
    created_at      = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at      = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    tiempo_trabajo  = db.Column(db.Time(), nullable=True)
    estado          = db.Column(db.Boolean(), nullable=True, default=True)
    usuario_id      = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    usuario         = db.relationship("Usuario", back_populates="asistencias")





    