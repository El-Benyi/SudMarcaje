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
    correo = db.Column(db.String(255), nullable=True, unique=True)
    clave = db.Column(db.String(255), nullable=True)
    
    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)
    
    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)
    
    # Sobrescribe el método `save` o crea uno personalizado
    def save(self):
        # Guarda o actualiza el usuario
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
    __tablename__ = "asistencia"
    id            = db.Column(db.Integer, primary_key = True)
    hora_inicio   = db.Column(db.Time(), nullable=False)
    hora_termino  = db.Column(db.Time(), nullable=False)
    hora_registro = db.Column(db.Time(), nullable=False, default=func.now())
    turno         = db.Column(db.String(255), nullable=False)

    created_at    = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at    = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now()) 

    
    usuario_id    = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario       = db.relationship("Usuario", back_populates="asistencias")





    