from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.estudiantes_model import EstudiantesModel
from helpers import str_clean
from security import permission_required

estudiantes_bp = Blueprint('estudiantes', __name__)


def login_required():
    if not session.get('activo'):
        return redirect(url_for('index'))
    return None


@estudiantes_bp.route('/')
def index():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = EstudiantesModel()
    perm = m.verificar_permisos(id_user, "Estudiantes")
    if not perm and id_user != 1:
        return render_template('permisos.html')
    return render_template('estudiantes/index.html')


@estudiantes_bp.route('/listar')
@permission_required('Estudiantes')
def listar():
    redir = login_required()
    if redir:
        return redir
    m = EstudiantesModel()
    data = m.get_estudiantes()
    for row in data:
        row['estadoLabel'] = 'Activo' if row['estado'] == 1 else 'Inactivo'
        row['acciones'] = 'editar,eliminar' if row['estado'] == 1 else 'reingresar'
    return jsonify(data)


@estudiantes_bp.route('/registrar', methods=['POST'])
@permission_required('Estudiantes')
def registrar():
    redir = login_required()
    if redir:
        return redir
    codigo = str_clean(request.form.get('codigo', ''))
    dni = str_clean(request.form.get('dni', ''))
    nombre = str_clean(request.form.get('nombre', ''))
    carrera = str_clean(request.form.get('carrera', ''))
    direccion = str_clean(request.form.get('direccion', ''))
    telefono = str_clean(request.form.get('telefono', ''))
    id_ = str_clean(request.form.get('id', ''))
    if not codigo or not nombre:
        return jsonify({'msg': 'Los campos código y nombre son requeridos', 'icono': 'warning'})
    m = EstudiantesModel()
    if id_ == '':
        data = m.insertar_estudiante(codigo, dni, nombre, carrera, direccion, telefono)
        msgs = {'ok': ('Estudiante registrado', 'success'),
                'existe': ('El código ya existe', 'warning'),
                'error': ('Error al registrar', 'error')}
        msg, icono = msgs.get(data, ('Error', 'error'))
        return jsonify({'msg': msg, 'icono': icono})
    else:
        data = m.actualizar_estudiante(codigo, dni, nombre, carrera, direccion, telefono, id_)
        if data == 'modificado':
            return jsonify({'msg': 'Estudiante modificado', 'icono': 'success'})
        return jsonify({'msg': 'Error al modificar', 'icono': 'error'})


@estudiantes_bp.route('/editar/<int:id_>')
@permission_required('Estudiantes')
def editar(id_):
    redir = login_required()
    if redir:
        return redir
    return jsonify(EstudiantesModel().edit_estudiante(id_))


@estudiantes_bp.route('/eliminar/<int:id_>')
@permission_required('Estudiantes')
def eliminar(id_):
    redir = login_required()
    if redir:
        return redir
    data = EstudiantesModel().estado_estudiante(0, id_)
    if data == 1:
        return jsonify({'msg': 'Estudiante dado de baja', 'icono': 'success'})
    return jsonify({'msg': 'Error al eliminar', 'icono': 'error'})


@estudiantes_bp.route('/reingresar/<int:id_>')
@permission_required('Estudiantes')
def reingresar(id_):
    redir = login_required()
    if redir:
        return redir
    data = EstudiantesModel().estado_estudiante(1, id_)
    if data == 1:
        return jsonify({'msg': 'Estudiante restaurado', 'icono': 'success'})
    return jsonify({'msg': 'Error al restaurar', 'icono': 'error'})


@estudiantes_bp.route('/buscarEstudiante')
@permission_required('Estudiantes')
def buscar_estudiante():
    redir = login_required()
    if redir:
        return redir
    valor = request.args.get('es', '')
    return jsonify(EstudiantesModel().buscar_estudiante(valor))
