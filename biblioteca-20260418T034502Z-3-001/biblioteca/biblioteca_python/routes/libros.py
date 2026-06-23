import os
import re
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, current_app
from models.libros_model import LibrosModel
from helpers import str_clean
from security import permission_required

libros_bp = Blueprint('libros', __name__)

def normalize_anio_edicion(value: str) -> str:
    value = value.strip()
    if not value:
        return ''
    if re.fullmatch(r'\d{4}', value):
        return f"{value}-01-01"
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return value
    return ''


def login_required():
    if not session.get('activo'):
        return redirect(url_for('index'))
    return None


@libros_bp.route('/')
def index():
    redir = login_required()
    if redir:
        return redir
    id_user = session['id_usuario']
    m = LibrosModel()
    perm = m.verificar_permisos(id_user, "Libros")
    if not perm and id_user != 1:
        return render_template('permisos.html')
    return render_template('libros/index.html')


@libros_bp.route('/listar')
@permission_required('Libros')
def listar():
    redir = login_required()
    if redir:
        return redir
    m = LibrosModel()
    data = m.get_libros()
    for row in data:
        row['estadoLabel'] = 'Activo' if row['estado'] == 1 else 'Inactivo'
        row['acciones'] = 'editar,eliminar' if row['estado'] == 1 else 'reingresar'
    return jsonify(data)


@libros_bp.route('/registrar', methods=['POST'])
@permission_required('Libros')
def registrar():
    redir = login_required()
    if redir:
        return redir
    titulo = str_clean(request.form.get('titulo', ''))
    autor = str_clean(request.form.get('autor', ''))
    editorial = str_clean(request.form.get('editorial', ''))
    materia = str_clean(request.form.get('materia', ''))
    cantidad = str_clean(request.form.get('cantidad', ''))
    num_pagina = str_clean(request.form.get('num_pagina', ''))
    anio_edicion = str_clean(request.form.get('anio_edicion', ''))
    descripcion = str_clean(request.form.get('descripcion', ''))
    id_ = str_clean(request.form.get('id', ''))

    if not titulo or not autor or not editorial or not materia or not cantidad or not num_pagina or not anio_edicion:
        return jsonify({'msg': 'Todos los campos son requeridos', 'icono': 'warning'})
    anio_edicion = normalize_anio_edicion(anio_edicion)
    if not anio_edicion:
        return jsonify({'msg': 'Anio de edicion invalido. Usa AAAA o AAAA-MM-DD', 'icono': 'warning'})
    try:
        cantidad_int = int(cantidad)
        num_pagina_int = int(num_pagina)
    except ValueError:
        return jsonify({'msg': 'Cantidad y paginas deben ser numericas', 'icono': 'warning'})
    if cantidad_int <= 0 or num_pagina_int <= 0:
        return jsonify({'msg': 'Cantidad y paginas deben ser mayores a 0', 'icono': 'warning'})

    img = request.files.get('imagen')
    img_nombre = 'logo.png'
    upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'libros')
    os.makedirs(upload_folder, exist_ok=True)

    if img and img.filename:
        ext = img.filename.rsplit('.', 1)[-1].lower()
        if ext not in ('png', 'jpg', 'jpeg'):
            return jsonify({'msg': 'Archivo no permitido', 'icono': 'warning'})
        img_nombre = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    elif request.form.get('foto_actual'):
        img_nombre = request.form.get('foto_actual')

    m = LibrosModel()
    if id_ == '':
        data = m.insertar_libros(titulo, autor, editorial, materia, cantidad_int,
                                 num_pagina_int, anio_edicion, descripcion, img_nombre)
        if data == 'ok':
            if img and img.filename:
                img.save(os.path.join(upload_folder, img_nombre))
            return jsonify({'msg': 'Libro registrado', 'icono': 'success'})
        elif data == 'existe':
            return jsonify({'msg': 'El libro ya existe', 'icono': 'warning'})
        return jsonify({'msg': 'Error al registrar', 'icono': 'error'})
    else:
        data = m.actualizar_libros(titulo, autor, editorial, materia, cantidad_int,
                                   num_pagina_int, anio_edicion, descripcion, img_nombre, id_)
        if data == 'modificado':
            if img and img.filename:
                img.save(os.path.join(upload_folder, img_nombre))
            return jsonify({'msg': 'Libro modificado', 'icono': 'success'})
        return jsonify({'msg': 'Error al modificar', 'icono': 'error'})


@libros_bp.route('/editar/<int:id_>')
@permission_required('Libros')
def editar(id_):
    redir = login_required()
    if redir:
        return redir
    m = LibrosModel()
    return jsonify(m.edit_libros(id_))


@libros_bp.route('/eliminar/<int:id_>')
@permission_required('Libros')
def eliminar(id_):
    redir = login_required()
    if redir:
        return redir
    m = LibrosModel()
    data = m.estado_libros(0, id_)
    if data == 1:
        return jsonify({'msg': 'Libro dado de baja', 'icono': 'success'})
    return jsonify({'msg': 'Error al eliminar', 'icono': 'error'})


@libros_bp.route('/reingresar/<int:id_>')
@permission_required('Libros')
def reingresar(id_):
    redir = login_required()
    if redir:
        return redir
    m = LibrosModel()
    data = m.estado_libros(1, id_)
    if data == 1:
        return jsonify({'msg': 'Libro restaurado', 'icono': 'success'})
    return jsonify({'msg': 'Error al restaurar', 'icono': 'error'})


@libros_bp.route('/verificar/<int:id_>')
@permission_required('Libros')
def verificar(id_):
    redir = login_required()
    if redir:
        return redir
    m = LibrosModel()
    data = m.edit_libros(id_)
    if data:
        return jsonify({'cantidad': data['cantidad'], 'icono': 'success'})
    return jsonify({'msg': 'Error Fatal', 'icono': 'error'})


@libros_bp.route('/buscarLibro')
@permission_required('Libros')
def buscar_libro():
    redir = login_required()
    if redir:
        return redir
    valor = request.args.get('lb', '')
    m = LibrosModel()
    return jsonify(m.buscar_libro(valor))
