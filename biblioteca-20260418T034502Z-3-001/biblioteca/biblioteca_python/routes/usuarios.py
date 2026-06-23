from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.usuarios_model import UsuariosModel
from helpers import str_clean
from security import SecurityUtils, login_required, permission_required
from logger import get_logger
from exceptions import ValidationError, AuthenticationError

usuarios_bp = Blueprint('usuarios', __name__)
logger = get_logger('app')


@usuarios_bp.route('/')
@login_required
def index():
    try:
        id_user = session['id_usuario']
        m = UsuariosModel()
        perm = m.verificar_permisos(id_user, "Usuarios")
        if not perm and id_user != 1:
            return render_template('permisos.html')
        return render_template('usuarios/index.html')
    except Exception as e:
        logger.error(f"Error in usuarios index: {e}")
        return render_template('permisos.html')


@usuarios_bp.route('/listar')
@login_required
@permission_required('Usuarios')
def listar():
    try:
        m = UsuariosModel()
        data = m.get_usuarios()
        for row in data:
            if row['estado'] == 1:
                if row['id'] != 1:
                    row['estadoLabel'] = 'Activo'
                    row['acciones'] = 'editar,eliminar,roles'
                else:
                    row['estadoLabel'] = 'Activo'
                    row['acciones'] = 'superadmin'
            else:
                row['estadoLabel'] = 'Inactivo'
                row['acciones'] = 'reingresar'
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in listar: {e}")
        return jsonify({'error': 'Error al listar usuarios'}), 500


@usuarios_bp.route('/validar', methods=['POST'])
def validar():
    try:
        usuario = SecurityUtils.sanitize_input(request.form.get('usuario', ''))
        clave = request.form.get('clave', '')

        if not usuario or not clave:
            raise ValidationError('Todos los campos son requeridos')

        m = UsuariosModel()
        data = m.get_usuario(usuario, clave)
        if data:
            permisos = [row['nombre'] for row in m.get_permisos_usuario(data['id'])]
            session['id_usuario'] = data['id']
            session['usuario'] = data['usuario']
            session['nombre'] = data['nombre']
            session['activo'] = True
            session['permisos'] = permisos
            logger.info(f"User {usuario} logged in successfully")
            return jsonify({'msg': 'Procesando', 'icono': 'success'})

        logger.warning(f"Failed login attempt for user {usuario}")
        raise AuthenticationError('Usuario o contraseña incorrecta')

    except ValidationError as e:
        return jsonify({'msg': e.message, 'icono': 'warning'}), e.code
    except AuthenticationError as e:
        return jsonify({'msg': e.message, 'icono': 'warning'}), e.code
    except Exception as e:
        logger.error(f"Error in validar: {e}")
        return jsonify({'msg': 'Error en autenticación', 'icono': 'error'}), 500


@usuarios_bp.route('/registrar', methods=['POST'])
@login_required
@permission_required('Usuarios')
def registrar():
    try:
        usuario = SecurityUtils.sanitize_input(request.form.get('usuario', ''))
        nombre = SecurityUtils.sanitize_input(request.form.get('nombre', ''))
        clave = request.form.get('clave', '')
        confirmar = request.form.get('confirmar', '')
        id_ = request.form.get('id', '')

        if not usuario or not nombre:
            raise ValidationError('Usuario y nombre son requeridos')

        m = UsuariosModel()

        if id_ == '':
            if not clave or not confirmar:
                raise ValidationError('La contraseña es requerida')
            if clave != confirmar:
                raise ValidationError('Las contraseñas no coinciden')

            is_strong, msg = SecurityUtils.validate_password_strength(clave)
            if not is_strong:
                raise ValidationError(msg)

            data = m.registrar_usuario(usuario, nombre, clave)
            msgs = {
                'ok': ('Usuario registrado', 'success'),
                'existe': ('El usuario ya existe', 'warning'),
                'error': ('Error al registrar', 'error')
            }
            msg, icono = msgs.get(data, ('Error', 'error'))
            logger.info(f"User {usuario} registered by {session.get('usuario')}")
            return jsonify({'msg': msg, 'icono': icono})
        else:
            data = m.modificar_usuario(usuario, nombre, id_)
            if data == 'existe':
                return jsonify({'msg': 'El usuario ya existe', 'icono': 'warning'})
            if data == 'modificado':
                logger.info(f"User {id_} modified by {session.get('usuario')}")
                return jsonify({'msg': 'Usuario modificado', 'icono': 'success'})
            return jsonify({'msg': 'Error al modificar', 'icono': 'error'})

    except ValidationError as e:
        return jsonify({'msg': e.message, 'icono': 'warning'}), e.code
    except Exception as e:
        logger.error(f"Error in registrar: {e}")
        return jsonify({'msg': 'Error al registrar', 'icono': 'error'}), 500


@usuarios_bp.route('/editar/<int:id_>')
@login_required
@permission_required('Usuarios')
def editar(id_):
    try:
        m = UsuariosModel()
        result = m.editar_user(id_)
        if not result:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in editar: {e}")
        return jsonify({'error': 'Error al editar'}), 500


@usuarios_bp.route('/eliminar/<int:id_>')
@login_required
@permission_required('Usuarios')
def eliminar(id_):
    try:
        if id_ == 1:
            return jsonify({'msg': 'No puedes eliminar el admin', 'icono': 'warning'})

        m = UsuariosModel()
        data = m.accion_user(0, id_)
        if data == 1:
            logger.info(f"User {id_} deactivated by {session.get('usuario')}")
            return jsonify({'msg': 'Usuario dado de baja', 'icono': 'success'})
        return jsonify({'msg': 'Error al eliminar', 'icono': 'error'})
    except Exception as e:
        logger.error(f"Error in eliminar: {e}")
        return jsonify({'msg': 'Error al eliminar', 'icono': 'error'}), 500


@usuarios_bp.route('/reingresar/<int:id_>')
@login_required
@permission_required('Usuarios')
def reingresar(id_):
    try:
        m = UsuariosModel()
        data = m.accion_user(1, id_)
        if data == 1:
            logger.info(f"User {id_} reactivated by {session.get('usuario')}")
            return jsonify({'msg': 'Usuario restaurado', 'icono': 'success'})
        return jsonify({'msg': 'Error al restaurar', 'icono': 'error'})
    except Exception as e:
        logger.error(f"Error in reingresar: {e}")
        return jsonify({'msg': 'Error al restaurar', 'icono': 'error'}), 500


@usuarios_bp.route('/permisos/<int:id_>')
@login_required
@permission_required('Usuarios')
def permisos(id_):
    try:
        m = UsuariosModel()
        todos = m.get_permisos()
        asignados = m.get_detalle_permisos(id_)
        asignados_ids = {a['id_permiso'] for a in asignados}
        return jsonify({'permisos': todos, 'asignados': list(asignados_ids), 'id_usuario': id_})
    except Exception as e:
        logger.error(f"Error in permisos: {e}")
        return jsonify({'error': 'Error al obtener permisos'}), 500


@usuarios_bp.route('/registrarPermisos', methods=['POST'])
@login_required
@permission_required('Usuarios')
def registrar_permisos():
    try:
        id_user = request.form.get('id_usuario', '')
        permisos_list = request.form.getlist('permisos[]')

        if not id_user:
            raise ValidationError('ID de usuario requerido')

        m = UsuariosModel()
        m.delete_permisos(id_user)
        for permiso in permisos_list:
            m.actualizar_permisos(id_user, permiso)

        logger.info(f"Permissions updated for user {id_user} by {session.get('usuario')}")
        return jsonify({'msg': 'Permisos actualizados', 'icono': 'success'})
    except ValidationError as e:
        return jsonify({'msg': e.message, 'icono': 'warning'}), e.code
    except Exception as e:
        logger.error(f"Error in registrar_permisos: {e}")
        return jsonify({'msg': 'Error al registrar permisos', 'icono': 'error'}), 500


@usuarios_bp.route('/cambiarPas', methods=['POST'])
@login_required
def cambiar_pas():
    try:
        id_ = session['id_usuario']
        clave_actual = request.form.get('clave_actual', '')
        clave_nueva = request.form.get('clave_nueva', '')
        confirmar = request.form.get('confirmar', '')

        if not clave_actual or not clave_nueva:
            raise ValidationError('Campos requeridos')

        if clave_nueva != confirmar:
            raise ValidationError('Las contraseñas no coinciden')

        is_strong, msg = SecurityUtils.validate_password_strength(clave_nueva)
        if not is_strong:
            raise ValidationError(msg)

        m = UsuariosModel()
        user = m.editar_user(id_)

        if not user:
            raise ValidationError('Usuario no encontrado')

        if not SecurityUtils.verify_password(clave_actual, user['clave']):
            logger.warning(f"Invalid password change attempt for user {id_}")
            raise ValidationError('Contraseña actual incorrecta')

        data = m.actualizar_pass(clave_nueva, id_)
        if data == 'modificado':
            logger.info(f"Password changed for user {id_}")
            return jsonify({'msg': 'Contraseña modificada', 'icono': 'success'})
        return jsonify({'msg': 'Error al modificar', 'icono': 'warning'})

    except ValidationError as e:
        return jsonify({'msg': e.message, 'icono': 'warning'}), e.code
    except Exception as e:
        logger.error(f"Error in cambiar_pas: {e}")
        return jsonify({'msg': 'Error al cambiar contraseña', 'icono': 'error'}), 500


@usuarios_bp.route('/salir')
def salir():
    try:
        usuario = session.get('usuario', 'desconocido')
        session.clear()
        logger.info(f"User {usuario} logged out")
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error in salir: {e}")
        return redirect(url_for('index'))
