from logger import get_logger

logger = get_logger('app')

class BaseService:
    """Servicio base para lógica de negocio"""

    def __init__(self, model):
        self.model = model

    def paginate(self, items, page=1, per_page=10):
        """Paginar resultados"""
        total = len(items) if isinstance(items, list) else 0
        start = (page - 1) * per_page
        end = start + per_page

        paginated = items[start:end] if isinstance(items, list) else []
        total_pages = (total + per_page - 1) // per_page

        return {
            'items': paginated,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }

    def search(self, items, query, fields):
        """Buscar en items"""
        if not query:
            return items

        query = query.lower()
        results = []

        for item in items:
            for field in fields:
                if field in item:
                    value = str(item[field]).lower()
                    if query in value:
                        results.append(item)
                        break

        return results

    def filter_by_status(self, items, status=1):
        """Filtrar por estado"""
        if status is None:
            return items
        return [item for item in items if item.get('estado') == status]

    def handle_error(self, error, operation="operation"):
        """Manejo centralizado de errores"""
        logger.error(f"Error in {operation}: {error}")
        return {
            'success': False,
            'error': str(error),
            'code': 500
        }

class UsuariosService(BaseService):
    """Servicio de usuarios"""

    def listar_con_paginacion(self, page=1, per_page=10, search=None, status=None):
        try:
            users = self.model.get_usuarios()

            if status is not None:
                users = self.filter_by_status(users, status)

            if search:
                users = self.search(users, search, ['usuario', 'nombre'])

            return self.paginate(users, page, per_page)
        except Exception as e:
            return self.handle_error(e, "list_users_pagination")

    def crear_usuario(self, usuario, nombre, clave):
        try:
            result = self.model.registrar_usuario(usuario, nombre, clave)
            return {
                'success': result == 'ok',
                'message': 'Usuario creado' if result == 'ok' else 'Error al crear usuario',
                'code': 201 if result == 'ok' else 400
            }
        except Exception as e:
            return self.handle_error(e, "create_user")

    def actualizar_usuario(self, id_, usuario, nombre):
        try:
            result = self.model.modificar_usuario(usuario, nombre, id_)
            return {
                'success': result == 'modificado',
                'message': 'Usuario actualizado' if result == 'modificado' else 'Error',
                'code': 200 if result == 'modificado' else 400
            }
        except Exception as e:
            return self.handle_error(e, "update_user")

    def obtener_usuario(self, id_):
        try:
            user = self.model.editar_user(id_)
            return {
                'success': user is not None,
                'user': user if user else None,
                'code': 200 if user else 404
            }
        except Exception as e:
            return self.handle_error(e, "get_user")

    def desactivar_usuario(self, id_):
        try:
            result = self.model.accion_user(0, id_)
            return {
                'success': result == 1,
                'message': 'Usuario desactivado' if result == 1 else 'Error',
                'code': 200 if result == 1 else 400
            }
        except Exception as e:
            return self.handle_error(e, "deactivate_user")

class LibrosService(BaseService):
    """Servicio de libros"""

    def listar_con_paginacion(self, page=1, per_page=10, search=None, status=None):
        try:
            libros = self.model.get_libros()

            if status is not None:
                libros = self.filter_by_status(libros, status)

            if search:
                libros = self.search(libros, search, ['titulo', 'isbn'])

            return self.paginate(libros, page, per_page)
        except Exception as e:
            return self.handle_error(e, "list_books_pagination")

class EstudiantesService(BaseService):
    """Servicio de estudiantes"""

    def listar_con_paginacion(self, page=1, per_page=10, search=None, status=None):
        try:
            estudiantes = self.model.get_estudiantes()

            if status is not None:
                estudiantes = self.filter_by_status(estudiantes, status)

            if search:
                estudiantes = self.search(estudiantes, search, ['nombre', 'carnet'])

            return self.paginate(estudiantes, page, per_page)
        except Exception as e:
            return self.handle_error(e, "list_students_pagination")
