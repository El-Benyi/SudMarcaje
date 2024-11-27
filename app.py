"""
Archivo app.py: módulo principal de la aplicación.
"""
# Importamos librerias necesarias 
from flask import Flask, render_template, flash, redirect, request, url_for

from flask_sqlalchemy import SQLAlchemy #base de datos
from flask_migrate import Migrate #versiones de bases de datos
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

#Iniciación y configuración de la app
app = Flask(__name__) 
app.config["SECRET_KEY"] = "mi clave!"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/sudcap"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #iniciamos bases de datos

login_manager = LoginManager(app) #iniciamos uso de sesiones
login_manager.login_view = "auth"

#Importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioEditar, FormularioEditarPerfil, FormularioAsistencia
from models import Usuario, Asistencia
from controllers import ControladorUsuarios, ControladorAsistencia
import time

#Inicialización de versiones de la bases de datos
Migrate(app,db)

#Inicialización de login_manager y configuración
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/home")
    
    if form_registro == None:
        form_registro = FormularioRegistro()
    if form_acceso == None: 
        form_acceso = FormularioAcceso()
    return render_template("auth.html",form_registro=form_registro,form_acceso=form_acceso)

#La ruta registro recibe un formulario y guarda en la base de datos
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if current_user.status == 'Administrador':
        # Recibimos datos del formulario
        form  = FormularioRegistro()
        error = None 
        #Validos errores de formulario
        if form.validate_on_submit():
            print("form valido")
            flash("Form valido")
            status = form.status.data
            nombre = form.nombre.data
            cargo = form.cargo.data
            numero_t  = form.numero_t.data
            apellido_p = form.apellido_p.data
            apellido_m = form.apellido_m.data
            correo = form.correo.data 
            clave  = form.clave.data 
            #Consultamos si existe en la db 
            usuario = Usuario().obtener_por_correo(correo)
            if usuario is not None:
                error = f"El correo {correo} ya se encuentra registrado"
                print(error)
                flash(error)
                return(redirect("/"))
            else:
                flash(f'Registro solicitado para el usuario { correo }')
                #Utilización de un controlador entre Vista y Modelo
                ControladorUsuarios().crear_usuario(status, cargo,numero_t , nombre, apellido_p, apellido_m, correo, clave)
                #Generamos una instancia de datos            
                return redirect("/home")
        else:
            print("form invalido")
            flash("Form invalido")
            #devolvemos al índice con forumalario relleno
            return render_template("register.html", form_registro=form)
    else:
        return render_template("error.html")

#La ruta que nos hace el acceso (login)
@app.route("/login", methods=["POST"])
def login():
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        flash(f"Acceso solicitado para el usuario { form_acceso.correo.data }")

        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
        
        if usuario is not None:
            if usuario.chequeo_clave(form_acceso.clave.data):
                login_user(usuario)
                return(redirect("/home"))
            else:
                flash(f"Clave incorrecta")
                print(f"Clave incorrecta")
                return(redirect("/"))
        else:
            flash(f"El usuario no esta registrado")
            print(f"El usuario no esta registrado")
            return(redirect("/"))
    
@app.route("/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))

#Ruta que nos lleva al inicio del usuario
@app.route("/home")
@login_required
def home():
    usuario = current_user
    obtener = ControladorUsuarios.all_users()
    return render_template("index.html", obtener_usuarios=obtener, usuario=usuario)


@app.route("/update/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = FormularioEditar(obj=usuario)

    if form.validate_on_submit():
        usuario.status = form.status.data
        usuario.cargo = form.cargo.data
        usuario.correo = form.correo.data
        usuario.numero_t = form.numero_t.data
        
        if form.clave.data:
            usuario.establecer_clave(form.clave.data)
        
        # Utiliza el método `save` para manejar la lógica de Admin
        usuario.save()

        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("home"))

    return render_template("edit_user.html", form=form, usuario=usuario)


@app.route("/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = FormularioEditarPerfil(obj=usuario)

    if form.validate_on_submit():
        usuario.correo = form.correo.data
        usuario.numero_t = form.numero_t.data
        
        if form.clave.data:
            usuario.establecer_clave(form.clave.data)
        
        usuario.save()

        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("home"))

    return render_template("edit_profile.html", form=form, usuario=usuario)

@app.route("/mapa")
@login_required
def mapa():
    return render_template("map.html")

@app.route("/asistencia", methods=["GET", "POST"])
@login_required
def asistencia():
    hora_actual = time.strftime("%H:%M:%S")
    form_a = FormularioAsistencia()

    if form_a.validate_on_submit():
        user_mail = form_a.user_mail.data

        # Verificar si el usuario existe
        usuario = Usuario.query.filter_by(correo=user_mail).first()
        if not usuario:
            flash("El correo ingresado no pertenece a un usuario registrado.", "error")
            return redirect(url_for("asistencia"))

        hora_inicio = form_a.hora_inicio.data
        hora_fin = form_a.hora_fin.data
        turno = form_a.turno.data
        fecha_registro = form_a.fecha_registro.data
        hora_registro = form_a.hora_registro.data

        ControladorAsistencia().crear_asistencia(user_mail, hora_inicio, hora_fin, turno, fecha_registro, hora_registro)

        flash("Asistencia registrada exitosamente.", "success")
        return redirect(url_for("asistencia"))

    return render_template("asistencia.html", form_a=form_a, hora_actual=hora_actual)