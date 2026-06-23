from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.editorial_model import EditorialModel
from helpers import str_clean
from security import permission_required

editorial_bp = Blueprint('editorial', __name__)


def login_required():
    if not session.get('activo'):
        return redirect(url_for('index'))
    return None


@editorial_bp.route('/')
def index():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = EditorialModel()
    perm = m.verificar_permisos(id_user, "Editorial")
    if not perm and id_user != 1:
        return render_template('permisos.html')
    return render_template('editorial/index.html')


@editorial_bp.route('/listar')
@permission_required('Editorial')
def listar():
    redir = login_required()
    if redir:
        return redir
    data = EditorialModel().get_editorial()
    for row in data:
        row['estadoLabel'] = 'Activo' if row['estado'] == 1 else 'Inactivo'
        row['acciones'] = 'editar,eliminar' if row['estado'] == 1 else 'reingresar'
    return jsonify(data)


@editorial_bp.route('/registrar', methods=['POST'])
@permission_required('Editorial')
def registrar():
    redir = login_required()
    if redir:
        return redir
    editorial = str_clean(request.form.get('editorial', ''))
    id_ = str_clean(request.form.get('id', ''))
    if not editorial:
        return jsonify({'msg': 'El campo editorial es requerido', 'icono': 'warning'})
    m = EditorialModel()
    if id_ == '':
        data = m.insertar_editorial(editorial)
        msgs = {'ok': ('Editorial registrada', 'success'),
                'existe': ('La editorial ya existe', 'warning'),
                'error': ('Error al registrar', 'error')}
        msg, icono = msgs.get(data, ('Error', 'error'))
        return jsonify({'msg': msg, 'icono': icono})
    else:
        data = m.actualizar_editorial(editorial, id_)
        if data == 'modificado':
            return jsonify({'msg': 'Editorial modificada', 'icono': 'success'})
        return jsonify({'msg': 'Error al modificar', 'icono': 'error'})


@editorial_bp.route('/editar/<int:id_>')
@permission_required('Editorial')
def editar(id_):
    redir = login_required()
    if redir:
        return redir
    return jsonify(EditorialModel().edit_editorial(id_))


@editorial_bp.route('/eliminar/<int:id_>')
@permission_required('Editorial')
def eliminar(id_):
    redir = login_required()
    if redir:
        return redir
    data = EditorialModel().estado_editorial(0, id_)
    if data == 1:
        return jsonify({'msg': 'Editorial dada de baja', 'icono': 'success'})
    return jsonify({'msg': 'Error al eliminar', 'icono': 'error'})


@editorial_bp.route('/reingresar/<int:id_>')
@permission_required('Editorial')
def reingresar(id_):
    redir = login_required()
    if redir:
        return redir
    data = EditorialModel().estado_editorial(1, id_)
    if data == 1:
        return jsonify({'msg': 'Editorial restaurada', 'icono': 'success'})
    return jsonify({'msg': 'Error al restaurar', 'icono': 'error'})


@editorial_bp.route('/buscarEditorial')
@permission_required('Editorial')
def buscar_editorial():
    redir = login_required()
    if redir:
        return redir
    valor = request.args.get('ed', '')
    return jsonify(EditorialModel().buscar_editorial(valor))
