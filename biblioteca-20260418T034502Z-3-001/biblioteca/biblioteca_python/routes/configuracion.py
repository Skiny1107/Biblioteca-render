import os
import traceback
from datetime import date
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, current_app
from models.configuracion_model import ConfiguracionModel
from helpers import str_clean
from logger import get_logger

configuracion_bp = Blueprint('configuracion', __name__)
logger = get_logger('app')


def login_required():
    if not session.get('activo'):
        return redirect(url_for('index'))
    return None


@configuracion_bp.route('/')
def index():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = ConfiguracionModel()
    perm = m.verificar_permisos(id_user, "Configuracion")
    if not perm and id_user != 1:
        return render_template('permisos.html')
    data = m.select_configuracion()
    return render_template('configuracion/index.html', config=data)


@configuracion_bp.route('/actualizar', methods=['POST'])
def actualizar():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = ConfiguracionModel()
    perm = m.verificar_permisos(id_user, "Configuracion")
    if not perm and id_user != 1:
        return jsonify({'msg': 'Sin permisos', 'icono': 'warning'})
    id_ = str_clean(request.form.get('id', ''))
    nombre = str_clean(request.form.get('nombre', ''))
    telefono = str_clean(request.form.get('telefono', ''))
    direccion = str_clean(request.form.get('direccion', ''))
    correo = str_clean(request.form.get('correo', ''))
    if not id_ or not nombre or not telefono or not direccion or not correo:
        return jsonify({'msg': 'Todos los campos son requeridos', 'icono': 'warning'})
    img = request.files.get('imagen')
    img_nombre = 'logo.png'
    data = m.actualizar_config(nombre, telefono, direccion, correo, img_nombre, id_)
    if data == 'modificado':
        if img and img.filename:
            ext = img.filename.rsplit('.', 1)[-1].lower()
            if ext not in ('png', 'jpg', 'jpeg'):
                return jsonify({'msg': 'Archivo no permitido', 'icono': 'warning'})
            logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')
            img.save(logo_path)
        return jsonify({'msg': 'Datos de la empresa modificados', 'icono': 'success'})
    return jsonify({'msg': 'Error al modificar', 'icono': 'error'})


@configuracion_bp.route('/admin')
def admin():
    try:
        redir = login_required()
        if redir:
            return redir

        m = ConfiguracionModel()
        data = {}
        tablas = {
            'libros': 'libro',
            'materias': 'materia',
            'estudiantes': 'estudiante',
            'autor': 'autor',
            'editorial': 'editorial',
            'prestamos': 'prestamo',
            'usuarios': 'usuarios',
        }

        for clave, tabla in tablas.items():
            try:
                data[clave] = m.select_datos(tabla) or {'total': 0}
            except Exception as e:
                logger.error(f"Error loading dashboard metric '{tabla}': {e}")
                data[clave] = {'total': 0}

        return render_template('configuracion/home.html', data=data)
    except Exception:
        debug_path = os.path.join(current_app.root_path, '..', 'temp', 'config_admin_traceback.txt')
        with open(debug_path, 'a', encoding='utf-8') as fh:
            fh.write(traceback.format_exc())
            fh.write("\n---\n")
        raise


@configuracion_bp.route('/grafico')
def grafico():
    redir = login_required()
    if redir:
        return redir
    return jsonify(ConfiguracionModel().get_reportes())


@configuracion_bp.route('/error')
def error():
    return render_template('configuracion/error.html')


@configuracion_bp.route('/vacio')
def vacio():
    return render_template('configuracion/vacio.html')


@configuracion_bp.route('/verificar')
def verificar():
    redir = login_required()
    if redir:
        return redir
    today = date.today().isoformat()
    data = ConfiguracionModel().get_verificar_prestamos(today)
    return jsonify(data)
