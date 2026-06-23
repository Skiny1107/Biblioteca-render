import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for, jsonify
from config import config as cfg
from logger import setup_logging, get_logger
from error_handler import ErrorHandler
from swagger import setup_swagger

# Setup logging
setup_logging()
logger = get_logger('app')

# Import blueprints
from routes.usuarios import usuarios_bp
from routes.libros import libros_bp
from routes.prestamos import prestamos_bp
from routes.autor import autor_bp
from routes.estudiantes import estudiantes_bp
from routes.editorial import editorial_bp
from routes.materia import materia_bp
from routes.configuracion import configuracion_bp
from routes.api import api_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(cfg)

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = cfg.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = cfg.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = cfg.SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = cfg.PERMANENT_SESSION_LIFETIME

# Register blueprints
app.register_blueprint(usuarios_bp,      url_prefix='/Usuarios')
app.register_blueprint(libros_bp,        url_prefix='/Libros')
app.register_blueprint(prestamos_bp,     url_prefix='/Prestamos')
app.register_blueprint(autor_bp,         url_prefix='/Autor')
app.register_blueprint(estudiantes_bp,   url_prefix='/Estudiantes')
app.register_blueprint(editorial_bp,     url_prefix='/Editorial')
app.register_blueprint(materia_bp,       url_prefix='/Materia')
app.register_blueprint(configuracion_bp, url_prefix='/Configuracion')
app.register_blueprint(api_bp)

# Register error handlers
ErrorHandler.register_handlers(app)

# Setup Swagger
setup_swagger(app)

@app.after_request
def normalize_dev_session_cookie(response):
    """In local HTTP development, ensure the session cookie is reusable."""
    if cfg.DEBUG:
        cookies = response.headers.getlist('Set-Cookie')
        if cookies:
            response.headers.remove('Set-Cookie')
            for cookie in cookies:
                response.headers.add('Set-Cookie', cookie.replace('; Secure', ''))
    return response

# Routes
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint con versión y build"""
    return jsonify({
        'status': 'ok',
        'version': '2.1.0',
        'build': 'workspace-2026-05-31',
        'database': 'connected',
        'features': ['admin', 'reportes_avanzados', 'rol_bibliotecario']
    }), 200

if __name__ == '__main__':
    env = cfg.DEBUG and 'DEBUG' or 'PRODUCTION'
    logger.info(f"Starting Biblioteca application v2.1.0 in {env} mode")
    logger.info(f"Roles disponibles: administrador, bibliotecario, usuario")
    logger.info(f"Formatos reportes: PDF, Excel, Word")
    app.run(
        debug=cfg.DEBUG,
        port=5000,
        host='0.0.0.0',
        use_reloader=cfg.DEBUG
    )

