"""
Archivo app.py: módulo principal de la aplicación.
"""
# Importamos librerias necesarias 
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy #base de datos
from flask_migrate import Migrate #versiones de bases de datos
from flask_login import LoginManager, login_user, logout_user, current_user, login_required



#
#app = Flask(__name__) 
#app.config["SECRET_KEY"] = "sud_marcaje2025"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:sud_marcaje2025@localhost:3306/sud_marcaje"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app) #iniciamos bases de datos


#Iniciación y configuración de la app
app = Flask(__name__) 
app.config["SECRET_KEY"] = "mi clave!"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/suda_marcaje"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #iniciamos bases de datos

login_manager = LoginManager(app) #iniciamos uso de sesiones
login_manager.login_view = "auth"

#Importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioEditar, FormularioEditarPerfil, FormularioAsistencia
from models import Usuario, Asistencia
from controllers import ControladorUsuarios, ControladorAsistencia
import time
from datetime import datetime

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
        
        form  = FormularioRegistro()
        error = None 

        if form.validate_on_submit():
            print("form valido")
            flash("Form valido")
            status = form.status.data
            nombre = form.nombre.data
            cargo = form.cargo.data
            numero_t  = form.numero_t.data
            apellido_p = form.apellido_p.data
            apellido_m = form.apellido_m.data
            work = form.work.data
            correo = form.correo.data 
            clave  = form.clave.data 

            usuario = Usuario().obtener_por_correo(correo)
            if usuario is not None:
                error = f"El correo {correo} ya se encuentra registrado"
                print(error)
                flash(error)
                return(redirect("/"))
            else:
                flash(f'Registro solicitado para el usuario { correo }')
                ControladorUsuarios().crear_usuario(status, cargo,numero_t , nombre, apellido_p, apellido_m,work, correo, clave)         
                return redirect("/register")
        else:
            print("form invalido")
            flash("Form invalido")
            return render_template("register.html", form_registro=form)
        
    else:
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/home")
@login_required
def home():
    form_a = FormularioAsistencia()
    asistencia = Asistencia.query.all()
    return render_template("index.html", form_a=form_a, asistencia=asistencia)


@app.route("/update/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = FormularioEditar(obj=usuario)
    if current_user.status == "Administrador":
        if form.validate_on_submit():
            usuario.status = form.status.data
            usuario.cargo = form.cargo.data
            usuario.work = form.work.data
            usuario.correo = form.correo.data
            usuario.numero_t = form.numero_t.data
            
            if form.clave.data:
                usuario.establecer_clave(form.clave.data)
            usuario.save()

            return redirect(url_for("home"))
        return render_template("edit_user.html", form=form, usuario=usuario)
    else:
        return redirect("/")



@app.route("/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if current_user.id != usuario.id:
        return redirect("/")  

    form = FormularioEditarPerfil(obj=usuario)
    
    if form.validate_on_submit():
        usuario.work = form.work.data
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
    if current_user.status == "Administrador":
        
        return render_template("map.html")
    else:
        
        return redirect("/")

@app.route("/asistencia", methods=["POST"])
def asistencia():
    try:
        data = request.get_json()
        
        latitud = data.get("latitud")
        longitud = data.get("longitud")
        turno = data.get("turno")
        fecha_registro = data.get("fecha_registro")
        hora_inicio = data.get("hora_inicio")
        hora_fin = data.get("hora_fin")
        tiempo_trabajo = data.get("tiempo_trabajo")
        usuario_id = data.get("usuario_id")

        # Si la hora de inicio se recibe, es para un nuevo turno (estado True)
        if hora_inicio and not hora_fin:
            nueva_asistencia = Asistencia(
                fecha_registro=datetime.strptime(fecha_registro, "%Y-%m-%d").date(),
                turno=turno,
                hora_inicio=hora_inicio,
                latitud=latitud,
                longitud=longitud,
                estado=True,
                usuario_id=usuario_id
            )
            db.session.add(nueva_asistencia)
            db.session.commit()
            return jsonify({"message": "Turno iniciado correctamente"}), 201

        # Si se recibe hora de fin, es para finalizar el turno (estado False)
        if hora_fin:
            asistencia = Asistencia.query.filter_by(hora_inicio=hora_inicio, estado=True).first()
            if asistencia:
                asistencia.hora_fin = hora_fin
                asistencia.tiempo_trabajo = tiempo_trabajo  # Aquí deberías manejar el formato correctamente
                asistencia.estado = False  # Cambiar el estado a False (turno finalizado)
                db.session.commit()
                return jsonify({"message": "Turno finalizado correctamente"}), 200
            else:
                return jsonify({"error": "No se encontró el turno para finalizar"}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Hubo un problema al registrar la asistencia"}), 500

@app.route('/finalizar_asistencia/<int:id>', methods=['POST'])
def finalizar_asistencia(id):
    asistencia = Asistencia.query.get_or_404(id)
    
    asistencia.hora_fin = datetime.now()

    db.session.commit()

    return redirect(url_for('home'))

@app.route('/api/coordenadas', methods=['GET'])
@login_required
def obtener_coordenadas():
    if current_user.status == 'Administrador':
        asistencias = Asistencia.query.all()  
    else:
        asistencias = Asistencia.query.filter_by(usuario_id=current_user.id).all()
    
    coordenadas = []

    for asistencia in asistencias:
        usuario = asistencia.usuario 
        coordenadas.append({
            'nombre': f"{usuario.nombre} {usuario.apellido_p} {usuario.apellido_m}",
            'lat': asistencia.latitud,
            'lon': asistencia.longitud,
            'fecha': asistencia.created_at.strftime('%Y-%m-%dT%H:%M:%S'), 
            'ini': str(asistencia.hora_inicio),
            'fin': str(asistencia.hora_fin),
            'tiempo_trabajo': str(asistencia.tiempo_trabajo),
            'estado': asistencia.estado 
        })

    return jsonify(coordenadas)




@app.route("/horario", methods=["GET"])
@login_required
def horarios():
    obtener = ControladorAsistencia.all_asistencias()

    usuarios = []
    if current_user.status == "Administrador":
        usuarios_ids = set()
        for asistencia in obtener:
            if asistencia.usuario.id not in usuarios_ids:
                usuarios_ids.add(asistencia.usuario.id)
                usuarios.append(asistencia.usuario)

    asistencias = Asistencia.query.filter_by(usuario_id=current_user.id).all()
    return render_template(
        "horarios.html",
        asistencias=asistencias,
        obtener_asistencias=obtener,
        usuarios=usuarios,  # Lista de usuarios únicos
    )

@app.route("/eliminar/<int:user_id>", methods=["POST", "GET"])
@login_required
def eliminar(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    
    asistencias = Asistencia.query.filter_by(usuario_id=usuario.id).all()
    
    for asistencia in asistencias:
        db.session.delete(asistencia)
    
    db.session.delete(usuario)
    
    db.session.commit()
    
    return redirect("/home")

@app.route('/check_email')
def check_email():
    email = request.args.get('email', '').lower()
    usuarios = Usuario.query.filter(Usuario.correo.like(f'{email}%')).all()
    suggestions = [user.correo for user in usuarios]
    
    return jsonify({'suggestions': suggestions})

@app.route("/trabajadores")
@login_required
def asistencias():
    usuario = current_user
    obtener = ControladorUsuarios.all_users()

    if current_user.status != "Administrador":
        return redirect(url_for("home"))

    return render_template("trabajadores.html", obtener_usuarios=obtener, usuario=usuario)