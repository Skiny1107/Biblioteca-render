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

class ErrorHandler:
    """Manejador centralizado de errores"""

    @staticmethod
    def register_handlers(app):
        """Registrar todos los manejadores de error"""

        @app.errorhandler(BibliotecaException)
        def handle_biblioteca_exception(error):
            logger.warning(f"BibliotecaException: {error.message}")
            return jsonify({
                'success': False,
                'error': error.message,
                'code': error.code
            }), error.code

        @app.errorhandler(400)
        def handle_bad_request(error):
            logger.warning(f"Bad request: {error.description}")
            return jsonify({
                'success': False,
                'error': 'Solicitud inválida',
                'code': 400
            }), 400

        @app.errorhandler(404)
        def handle_not_found(error):
            logger.warning(f"Not found: {error.description}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 404
            return jsonify({
                'success': False,
                'error': 'No encontrado',
                'code': 404
            }), 404

        @app.errorhandler(405)
        def handle_method_not_allowed(error):
            logger.warning(f"Method not allowed: {request.method} {request.path}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 405
            return jsonify({
                'success': False,
                'error': 'Método no permitido',
                'code': 405
            }), 405

        @app.errorhandler(429)
        def handle_rate_limit(error):
            logger.warning(f"Rate limit exceeded: {request.method} {request.path}")
            if _prefers_html():
                return render_template('configuracion/error.html'), 429
            return jsonify({
                'success': False,
                'error': 'Demasiadas solicitudes. Intenta de nuevo en un momento',
                'code': 429
            }), 429

        @app.errorhandler(500)
        def handle_internal_error(error):
            logger.error(f"Internal server error: {error}\n{traceback.format_exc()}")
            _write_debug_trace("500", error)
            if _prefers_html():
                return render_template('configuracion/error.html'), 500
            return jsonify({
                'success': False,
                'error': 'Error interno del servidor',
                'code': 500
            }), 500

        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            logger.error(f"Unexpected error: {error}\n{traceback.format_exc()}")
            _write_debug_trace("Exception", error)
            if _prefers_html():
                return render_template('configuracion/error.html'), 500
            return jsonify({
                'success': False,
                'error': 'Error inesperado',
                'code': 500
            }), 500

def handle_route_errors(f):
    """Decorador para manejar errores en rutas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BibliotecaException as e:
            logger.warning(f"BibliotecaException in {f.__name__}: {e.message}")
            return jsonify({'success': False, 'error': e.message, 'code': e.code}), e.code
        except ValueError as e:
            logger.warning(f"ValueError in {f.__name__}: {e}")
            return jsonify({'success': False, 'error': str(e), 'code': 400}), 400
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}\n{traceback.format_exc()}")
            return jsonify({'success': False, 'error': 'Error interno', 'code': 500}), 500
    return decorated_function

def log_request(f):
    """Decorador para loguear requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"{request.method} {request.path} - IP: {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function
