import hashlib
import secrets
import re
from urllib.parse import urlparse
from functools import wraps
from flask import session, redirect, url_for, jsonify, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import config as cfg

# Definir roles del sistema
ROLES_SISTEMA = {
    'administrador': 1,
    'bibliotecario': 2,
    'usuario': 3
}

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
    def validate_text_length(value: str, min_len: int = 1, max_len: int = 255) -> bool:
        """Validar longitud de texto"""
        if not isinstance(value, str):
            return False
        value = value.strip()
        return min_len <= len(value) <= max_len

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validar formato de usuario"""
        pattern = r'^[a-zA-Z0-9_-]{3,20}$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_person_name(value: str, max_len: int = 120) -> bool:
        """Validar nombres con letras, espacios y signos comunes"""
        if not value:
            return False
        value = value.strip()
        if len(value) < 3 or len(value) > max_len:
            return False
        pattern = rf"^(?=.*[A-Za-zÁÉÍÓÚáéíóúÑñ])[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s.'-]{{2,{max_len - 1}}}$"
        return re.match(pattern, value) is not None

    @staticmethod
    def validate_generic_text(value: str, min_len: int = 2, max_len: int = 150) -> bool:
        """Validar textos generales para títulos, editoriales y materias"""
        pattern = rf'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,:;()&\-\'"/#]{{{min_len},{max_len}}}$'
        return re.match(pattern, value.strip()) is not None if value else False

    @staticmethod
    def validate_student_code(value: str) -> bool:
        """Validar código de estudiante"""
        pattern = r'^[A-Za-z0-9_-]{2,20}$'
        return re.match(pattern, value.strip()) is not None if value else False

    @staticmethod
    def validate_dni(value: str) -> bool:
        """Validar DNI o documento"""
        pattern = r'^[A-Za-z0-9-]{6,20}$'
        return re.match(pattern, value.strip()) is not None if value else False

    @staticmethod
    def validate_phone(value: str) -> bool:
        """Validar teléfono"""
        pattern = r'^[0-9+\-\s()]{7,20}$'
        return re.match(pattern, value.strip()) is not None if value else False

    @staticmethod
    def validate_url(value: str) -> bool:
        """Validar URL http/https"""
        try:
            parsed = urlparse(value.strip())
            return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
        except Exception:
            return False

    @staticmethod
    def validate_positive_int(value, min_value: int = 1, max_value: int = None) -> bool:
        """Validar enteros positivos"""
        try:
            number = int(value)
        except (TypeError, ValueError):
            return False
        if number < min_value:
            return False
        if max_value is not None and number > max_value:
            return False
        return True

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
                return jsonify({'success': False, 'msg': 'Tu sesión ha expirado. Inicia sesión de nuevo', 'icono': 'warning', 'error': 'No autenticado', 'code': 401}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para solo administrador (id=1)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('activo'):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'msg': 'Tu sesión ha expirado. Inicia sesión de nuevo', 'icono': 'warning', 'error': 'No autenticado', 'code': 401}), 401
            return redirect(url_for('login'))
        if session.get('id_usuario') != 1:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'msg': 'No tienes permisos para realizar esta acción', 'icono': 'warning', 'error': 'Acceso denegado', 'code': 403}), 403
            return render_template('permisos.html'), 403
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission_name):
    """Decorador para verificar permisos específicos."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('activo'):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'msg': 'Tu sesión ha expirado. Inicia sesión de nuevo', 'icono': 'warning', 'error': 'No autenticado', 'code': 401}), 401
                return redirect(url_for('login'))

            from models.usuarios_model import UsuariosModel
            user_id = session['id_usuario']
            session_permissions = set(session.get('permisos', []))
            m = UsuariosModel()

            if user_id == 1 or permission_name in session_permissions or m.verificar_permisos(user_id, permission_name):
                return f(*args, **kwargs)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'msg': 'No tienes permisos para realizar esta acción', 'icono': 'warning', 'error': 'Permiso denegado', 'code': 403}), 403
            return render_template('permisos.html'), 403
        return decorated_function
    return decorator
