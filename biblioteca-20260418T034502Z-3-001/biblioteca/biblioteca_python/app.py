import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from config import config as cfg, SECRET_KEY
from logger import setup_logging, get_logger
from exceptions import BibliotecaException, AuthenticationError, ValidationError
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

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(cfg)

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = cfg.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = cfg.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = cfg.SESSION_COOKIE_SAMESITE
app.config['PERMANENT_SESSION_LIFETIME'] = cfg.PERMANENT_SESSION_LIFETIME

# Security headers
if not cfg.DEBUG:
    Talisman(app,
        force_https=False,  # Set to True in production
        session_cookie_secure=cfg.SESSION_COOKIE_SECURE,
        strict_transport_security=True,
        content_security_policy={
            'default-src': "'self'",
            'script-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            'style-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            'img-src': ["'self'", "data:", "*"],
        }
    )

# CORS setup
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    # In local development the browser can quickly exceed very low limits
    # because each page load also fetches multiple static assets and AJAX calls.
    default_limits=["1000 per day", "300 per hour"] if cfg.DEBUG else ["200 per day", "50 per hour"],
    storage_uri=cfg.RATELIMIT_STORAGE_URL
)

app.limiter = limiter

# Register blueprints
app.register_blueprint(usuarios_bp,      url_prefix='/Usuarios')
app.register_blueprint(libros_bp,        url_prefix='/Libros')
app.register_blueprint(prestamos_bp,     url_prefix='/Prestamos')
app.register_blueprint(autor_bp,         url_prefix='/Autor')
app.register_blueprint(estudiantes_bp,   url_prefix='/Estudiantes')
app.register_blueprint(editorial_bp,     url_prefix='/Editorial')
app.register_blueprint(materia_bp,       url_prefix='/Materia')
app.register_blueprint(configuracion_bp, url_prefix='/Configuracion')

# Register error handlers
ErrorHandler.register_handlers(app)

# Setup Swagger
setup_swagger(app)

# Before request hook
@app.before_request
def before_request():
    from flask import session
    if session:
        session.permanent = True

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
def index():
    return render_template('index.html')

@app.route('/health')
@limiter.exempt
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'version': '1.0.0', 'build': 'workspace-2026-04-07'}), 200

if __name__ == '__main__':
    logger.info(f"Starting Biblioteca application in {cfg.DEBUG and 'DEBUG' or 'PRODUCTION'} mode")
    app.run(
        debug=cfg.DEBUG,
        port=5000,
        host='0.0.0.0',
        use_reloader=cfg.DEBUG
    )
