from flask import request, jsonify, render_template, current_app
from functools import wraps
from logger import get_logger
from exceptions import BibliotecaException
import traceback
import os

logger = get_logger('app')


def _prefers_html():
    return (
        request.headers.get('X-Requested-With') != 'XMLHttpRequest'
        and request.accept_mimetypes.accept_html
        and request.accept_mimetypes.accept_html >= request.accept_mimetypes.accept_json
    )


def _write_debug_trace(prefix, error):
    try:
        debug_dir = os.path.join(current_app.root_path, '..', 'temp')
        os.makedirs(debug_dir, exist_ok=True)
        debug_path = os.path.join(debug_dir, 'server_traceback.txt')
        with open(debug_path, 'a', encoding='utf-8') as fh:
            fh.write(f"{prefix}: {error}\n")
            fh.write(traceback.format_exc())
            fh.write("\n---\n")
    except Exception:
        pass


def _json_error(message, code, icono='warning'):
    return jsonify({
        'success': False,
        'msg': message,
        'icono': icono,
        'error': message,
        'code': code
    }), code


class ErrorHandler:
    """Manejador centralizado de errores"""

    @staticmethod
    def register_handlers(app):
        """Registrar todos los manejadores de error"""

        @app.errorhandler(BibliotecaException)
        def handle_biblioteca_exception(error):
            logger.warning(f"BibliotecaException: {error.message}")
            return _json_error(error.message, error.code, 'warning' if error.code < 500 else 'error')

        @app.errorhandler(400)
        def handle_bad_request(error):
            logger.warning(f"Bad request: {error.description}")
            return _json_error('Solicitud invalida', 400, 'warning')

        @app.errorhandler(404)
        def handle_not_found(error):
            logger.warning(f"Not found: {error.description}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 404
            return _json_error('No encontrado', 404, 'warning')

        @app.errorhandler(405)
        def handle_method_not_allowed(error):
            logger.warning(f"Method not allowed: {request.method} {request.path}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 405
            return _json_error('Metodo no permitido', 405, 'warning')

        @app.errorhandler(429)
        def handle_rate_limit(error):
            logger.warning(f"Rate limit exceeded: {request.method} {request.path}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 429
            return _json_error('Demasiadas solicitudes. Intenta de nuevo en un momento', 429, 'warning')

        @app.errorhandler(500)
        def handle_internal_error(error):
            logger.error(f"Internal server error: {error}\n{traceback.format_exc()}")
            _write_debug_trace("500", error)
            if _prefers_html():
                return render_template('configuracion/error.html'), 500
            return _json_error('Error interno del servidor', 500, 'error')

        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            logger.error(f"Unexpected error: {error}\n{traceback.format_exc()}")
            _write_debug_trace("Exception", error)
            if _prefers_html():
                return render_template('configuracion/error.html'), 500
            return _json_error('Error inesperado', 500, 'error')


def handle_route_errors(f):
    """Decorador para manejar errores en rutas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BibliotecaException as e:
            logger.warning(f"BibliotecaException in {f.__name__}: {e.message}")
            return _json_error(e.message, e.code, 'warning' if e.code < 500 else 'error')
        except ValueError as e:
            logger.warning(f"ValueError in {f.__name__}: {e}")
            return _json_error(str(e), 400, 'warning')
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}\n{traceback.format_exc()}")
            return _json_error('Error interno', 500, 'error')
    return decorated_function


def log_request(f):
    """Decorador para loguear requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"{request.method} {request.path} - IP: {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function
