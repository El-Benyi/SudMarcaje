"""
    Archivo donde se definen los formularios del sistema
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class FormularioRegistro(FlaskForm):    
    status = SelectField('Estatus del Usuario', 
                     choices=[('',''),('Normal', 'Normal'), ('Administrador', 'Administrador')], 
                     validators=[DataRequired()])
    numero_t            = StringField("Numero Telefonico", validators=[Length(min=9, max=9, message="El número debe tener exactamente 9 dígitos."),Regexp(r'^\d{9}$', message="El número debe contener solo 9 dígitos numéricos.")]) 
    nombre              = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    apellido_p          = StringField('Apellido P.', validators=[DataRequired(), Length(min=3)])
    apellido_m          = StringField('Apellido M.', validators=[DataRequired(), Length(min=3)])
    cargo               = StringField('Cargo.', validators=[DataRequired(), Length(min=3)])
    correo              = EmailField('Correo', validators=[DataRequired(), Email(), EqualTo('confirmar_correo', message="Los correos deben ser iguales.")])
    confirmar_correo    = EmailField('Confirmar correo', validators=[DataRequired(), Email(), EqualTo('correo', message="Los correos deben ser iguales.")])
    clave               = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirmar_clave', message="Las claves deben ser iguales.")])
    confirmar_clave     = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit              = SubmitField('Registrar Usuario')

class FormularioAcceso(FlaskForm):    
    correo = EmailField('Correo', validators=[DataRequired(), Email()])
    clave  = PasswordField('Contraseña', validators=[DataRequired()])    
    submit = SubmitField('Acceder')


class FormularioEditar(FlaskForm):
    status          = SelectField('Privilegios del Usuario', 
                     choices=[('',''),('Normal', 'Normal'), ('Administrador', 'Administrador')], 
                     validators=[DataRequired()])
    numero_t            = StringField("Numero Telefonico", validators=[Length(min=9, max=9, message="El número debe tener exactamente 9 dígitos."),Regexp(r'^\d{9}$', message="El número debe contener solo 9 dígitos numéricos.")]) 
    cargo               = StringField('Cargo.', validators=[DataRequired(), Length(min=3)])
    correo              = EmailField('Correo', validators=[Email()])
    clave               = PasswordField('Contraseña')
    submit              = SubmitField('Editar Usuario')

class FormularioEditarPerfil(FlaskForm):
    numero_t            = StringField("Numero Telefonico", validators=[Length(min=9, max=9, message="El número debe tener exactamente 9 dígitos."),Regexp(r'^\d{9}$', message="El número debe contener solo 9 dígitos numéricos.")]) 
    correo              = EmailField('Correo', validators=[Email()])
    clave               = PasswordField('Contraseña')
    submit              = SubmitField('Editar mi Perfil')

class FormularioAsistencia(FlaskForm):    
    user_mail           = EmailField('Buscar trabajador por correo', validators=[DataRequired()])
    hora_inicio         = TimeField('Inicio del Turno', validators=[DataRequired()])
    hora_fin            = TimeField('Fin del Turno', validators=[DataRequired()])
    turno               = SelectField(
                        'Turnos',
                        choices=[('diurno', 'Diurno (08:00 a 20:00 hrs)'),('nocturno', 'Nocturno (20:00 a 08:00 hrs)')],validators=[DataRequired()])
    fecha_registro      = DateTimeField('Fecha Registro', format='%Y-%m-%d', validators=[DataRequired()])
    hora_registro       = TimeField('Hora de Registro')
    submit              = SubmitField('Registrar Asistencia ')