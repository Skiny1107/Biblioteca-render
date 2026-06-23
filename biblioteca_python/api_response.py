from flask import jsonify
from datetime import datetime

class APIResponse:
    """Respuestas API estandarizadas"""

    @staticmethod
    def success(data=None, message="Success", code=200):
        """Respuesta exitosa"""
        return jsonify({
            'success': True,
            'message': message,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }), code

    @staticmethod
    def error(message="Error", code=400, error_code=None):
        """Respuesta de error"""
        return jsonify({
            'success': False,
            'message': message,
            'error_code': error_code or code,
            'timestamp': datetime.utcnow().isoformat()
        }), code

    @staticmethod
    def paginated(items, page, per_page, total, total_pages, message="Success"):
        """Respuesta paginada"""
        return jsonify({
            'success': True,
            'message': message,
            'data': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    @staticmethod
    def created(data, message="Created successfully"):
        """Respuesta de creación"""
        return APIResponse.success(data, message, 201)

    @staticmethod
    def no_content():
        """Respuesta sin contenido"""
        return '', 204

    @staticmethod
    def bad_request(message="Bad request"):
        """Bad request"""
        return APIResponse.error(message, 400)

    @staticmethod
    def unauthorized(message="Unauthorized"):
        """No autorizado"""
        return APIResponse.error(message, 401)

    @staticmethod
    def forbidden(message="Forbidden"):
        """Acceso prohibido"""
        return APIResponse.error(message, 403)

    @staticmethod
    def not_found(message="Resource not found"):
        """No encontrado"""
        return APIResponse.error(message, 404)

    @staticmethod
    def conflict(message="Resource already exists"):
        """Conflicto"""
        return APIResponse.error(message, 409)

    @staticmethod
    def server_error(message="Internal server error"):
        """Error del servidor"""
        return APIResponse.error(message, 500)
