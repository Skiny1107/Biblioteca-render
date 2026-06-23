class BibliotecaException(Exception):
    """Excepción base del proyecto"""
    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AuthenticationError(BibliotecaException):
    """Error de autenticación"""
    def __init__(self, message="Autenticación fallida"):
        super().__init__(message, 401)

class AuthorizationError(BibliotecaException):
    """Error de autorización"""
    def __init__(self, message="Acceso denegado"):
        super().__init__(message, 403)

class ValidationError(BibliotecaException):
    """Error de validación"""
    def __init__(self, message="Datos inválidos"):
        super().__init__(message, 400)

class ResourceNotFoundError(BibliotecaException):
    """Recurso no encontrado"""
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, 404)

class DatabaseError(BibliotecaException):
    """Error de base de datos"""
    def __init__(self, message="Error en base de datos"):
        super().__init__(message, 500)

class DuplicateResourceError(BibliotecaException):
    """Recurso duplicado"""
    def __init__(self, message="El recurso ya existe"):
        super().__init__(message, 409)

class OperationError(BibliotecaException):
    """Error en operación"""
    def __init__(self, message="Error en operación"):
        super().__init__(message, 500)
