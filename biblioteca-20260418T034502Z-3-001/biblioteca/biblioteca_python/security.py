import hashlib
import secrets
import re
from functools import wraps
from flask import session, redirect, url_for, jsonify, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import config as cfg

class SecurityUtils:
    """Utilidades de seguridad y validación"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de contraseña usando werkzeug"""
        return generate_password_hash(password, method='pbkdf2:sha256')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_token(data: dict, hours: int = None) -> str:
        """Generar JWT token"""
        hours = hours or cfg.JWT_EXPIRATION_HOURS
        payload = {
            'data': data,
            'exp': datetime.utcnow() + timedelta(hours=hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, cfg.JWT_SECRET, algorithm=cfg.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verificar y decodificar JWT token"""
        try:
            payload = jwt.decode(token, cfg.JWT_SECRET, algorithms=[cfg.JWT_ALGORITHM])
            return payload.get('data')
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def sanitize_input(value: str) -> str:
        """Sanitizar entrada de usuario"""
        if not isinstance(value, str):
            value = str(value)

        # Remover espacios en blanco excesivos
        value = re.sub(r'\s+', ' ', value).strip()

        # Remover etiquetas script y event handlers
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'on\w+\s*=',
            r'javascript:',
            r'eval\(',
            r'expression\(',
        ]
        for pattern in dangerous_patterns:
            value = re.sub(pattern, '', value, flags=re.IGNORECASE)

        return value

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validar formato de usuario"""
        pattern = r'^[a-zA-Z0-9_-]{3,20}$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_password_strength(password: str) -> tuple:
        """Validar fortaleza de contraseña"""
        if len(password) < 8:
            return False, "Mínimo 8 caracteres"
        if not re.search(r'[A-Z]', password):
            return False, "Debe contener mayúsculas"
        if not re.search(r'[a-z]', password):
            return False, "Debe contener minúsculas"
        if not re.search(r'[0-9]', password):
            return False, "Debe contener números"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Debe contener caracteres especiales"
        return True, "Contraseña fuerte"

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generar token seguro"""
        return secrets.token_urlsafe(length)

def login_required(f):
    """Decorador para rutas protegidas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('activo'):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'No autenticado', 'code': 401}), 401
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para solo admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('activo') or session.get('id_usuario') != 1:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Acceso denegado', 'code': 403}), 403
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission_name):
    """Decorador para verificar permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('activo'):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'No autenticado', 'code': 401}), 401
                return redirect(url_for('index'))

            from models.usuarios_model import UsuariosModel
            user_id = session['id_usuario']
            session_permissions = set(session.get('permisos', []))
            m = UsuariosModel()

            if user_id == 1 or permission_name in session_permissions or m.verificar_permisos(user_id, permission_name):
                return f(*args, **kwargs)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Permiso denegado', 'code': 403}), 403
            return render_template('permisos.html')
        return decorated_function
    return decorator
