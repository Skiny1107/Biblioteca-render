from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.materia_model import MateriaModel
from helpers import str_clean
from security import permission_required

materia_bp = Blueprint('materia', __name__)


def login_required():
    if not session.get('activo'):
        return redirect(url_for('index'))
    return None


@materia_bp.route('/')
def index():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = MateriaModel()
    perm = m.verificar_permisos(id_user, "Materias")
    if not perm and id_user != 1:
        return render_template('permisos.html')
    return render_template('materia/index.html')


@materia_bp.route('/listar')
@permission_required('Materias')
def listar():
    redir = login_required()
    if redir:
        return redir
    data = MateriaModel().get_materias()
    for row in data:
        row['estadoLabel'] = 'Activo' if row['estado'] == 1 else 'Inactivo'
        row['acciones'] = 'editar,eliminar' if row['estado'] == 1 else 'reingresar'
    return jsonify(data)


@materia_bp.route('/registrar', methods=['POST'])
@permission_required('Materias')
def registrar():
    redir = login_required()
    if redir:
        return redir
    materia = str_clean(request.form.get('materia', ''))
    id_ = str_clean(request.form.get('id', ''))
    if not materia:
        return jsonify({'msg': 'El campo materia es requerido', 'icono': 'warning'})
    m = MateriaModel()
    if id_ == '':
        data = m.insertar_materia(materia)
        msgs = {'ok': ('Materia registrada', 'success'),
                'existe': ('La materia ya existe', 'warning'),
                'error': ('Error al registrar', 'error')}
        msg, icono = msgs.get(data, ('Error', 'error'))
        return jsonify({'msg': msg, 'icono': icono})
    else:
        data = m.actualizar_materia(materia, id_)
        if data == 'modificado':
            return jsonify({'msg': 'Materia modificada', 'icono': 'success'})
        return jsonify({'msg': 'Error al modificar', 'icono': 'error'})


@materia_bp.route('/editar/<int:id_>')
@permission_required('Materias')
def editar(id_):
    redir = login_required()
    if redir:
        return redir
    return jsonify(MateriaModel().edit_materia(id_))


@materia_bp.route('/eliminar/<int:id_>')
@permission_required('Materias')
def eliminar(id_):
    redir = login_required()
    if redir:
        return redir
    data = MateriaModel().estado_materia(0, id_)
    if data == 1:
        return jsonify({'msg': 'Materia dada de baja', 'icono': 'success'})
    return jsonify({'msg': 'Error al eliminar', 'icono': 'error'})


@materia_bp.route('/reingresar/<int:id_>')
@permission_required('Materias')
def reingresar(id_):
    redir = login_required()
    if redir:
        return redir
    data = MateriaModel().estado_materia(1, id_)
    if data == 1:
        return jsonify({'msg': 'Materia restaurada', 'icono': 'success'})
    return jsonify({'msg': 'Error al restaurar', 'icono': 'error'})


@materia_bp.route('/buscarMateria')
@permission_required('Materias')
def buscar_materia():
    redir = login_required()
    if redir:
        return redir
    valor = request.args.get('ma', '')
    return jsonify(MateriaModel().buscar_materia(valor))
