import os
import traceback
from datetime import date
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, current_app
from models.configuracion_model import ConfiguracionModel
from helpers import str_clean
from logger import get_logger
from security import SecurityUtils

configuracion_bp = Blueprint('configuracion', __name__)
logger = get_logger('app')


def login_required():
    if not session.get('activo'):
        return redirect(url_for('login'))
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
    if not SecurityUtils.validate_generic_text(nombre, min_len=2, max_len=120):
        return jsonify({'msg': 'Ingresa un nombre valido para la empresa', 'icono': 'warning'})
    if not SecurityUtils.validate_phone(telefono):
        return jsonify({'msg': 'Ingresa un telefono valido', 'icono': 'warning'})
    if not SecurityUtils.validate_generic_text(direccion, min_len=3, max_len=150):
        return jsonify({'msg': 'Ingresa una direccion valida', 'icono': 'warning'})
    if not SecurityUtils.validate_email(correo):
        return jsonify({'msg': 'Ingresa un correo valido', 'icono': 'warning'})
    img = request.files.get('imagen')
    img_nombre = 'logo.png'
    data = m.actualizar_config(nombre, telefono, direccion, correo, img_nombre, id_)
    if data == 'modificado':
        if img and img.filename:
            ext = img.filename.rsplit('.', 1)[-1].lower()
            is_image = img.content_type and img.content_type.startswith('image/')
            allowed_exts = ('png', 'jpg', 'jpeg', 'webp', 'gif', 'avif', 'svg', 'bmp', 'tiff', 'jfif', 'ico', 'heic', 'heif')
            if not is_image and ext not in allowed_exts:
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

        today = date.today().isoformat()
        try:
            data['prestamos_activos'] = m.get_prestamos_activos_count() or {'total': 0}
            data['prestamos_vencidos'] = m.get_prestamos_vencidos_count(today) or {'total': 0}
            data['solicitudes_pendientes'] = m.get_solicitudes_pendientes_count() or {'total': 0}
            data['libros_agotados'] = m.get_libros_agotados_count() or {'total': 0}
        except Exception as e:
            logger.error(f"Error loading new metrics: {e}")
            data['prestamos_activos'] = {'total': 0}
            data['prestamos_vencidos'] = {'total': 0}
            data['solicitudes_pendientes'] = {'total': 0}
            data['libros_agotados'] = {'total': 0}

        return render_template('configuracion/home.html', data=data)
    except Exception:
        logger.exception("Error loading admin dashboard")
        raise


@configuracion_bp.route('/grafico')
def grafico():
    redir = login_required()
    if redir:
        return redir
    tipo = request.args.get('tipo', 'stock')
    return jsonify(ConfiguracionModel().get_reportes_dinamicos(tipo))


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
