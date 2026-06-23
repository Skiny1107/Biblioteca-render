from flask import Blueprint
from flasgger import Swagger

def setup_swagger(app):
    """Configurar Swagger en la aplicación"""
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Biblioteca API",
            "description": "API REST para Sistema de Gestión de Biblioteca",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
            }
        },
        "basePath": "/api/v1",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    })

    return swagger

USUARIOS_SCHEMAS = {
    'Usuario': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'usuario': {'type': 'string'},
            'nombre': {'type': 'string'},
            'estado': {'type': 'integer'}
        }
    },
    'UsuarioCreate': {
        'type': 'object',
        'required': ['usuario', 'nombre', 'clave'],
        'properties': {
            'usuario': {'type': 'string', 'minLength': 3},
            'nombre': {'type': 'string', 'minLength': 3},
            'clave': {'type': 'string', 'minLength': 8}
        }
    },
    'Paginated': {
        'type': 'object',
        'properties': {
            'success': {'type': 'boolean'},
            'data': {'type': 'array'},
            'pagination': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'},
                    'total': {'type': 'integer'},
                    'total_pages': {'type': 'integer'}
                }
            }
        }
    }
}

LIBROS_SCHEMAS = {
    'Libro': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'titulo': {'type': 'string'},
            'isbn': {'type': 'string'},
            'cantidad': {'type': 'integer'},
            'estado': {'type': 'integer'}
        }
    }
}

ESTUDIANTES_SCHEMAS = {
    'Estudiante': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'nombre': {'type': 'string'},
            'carnet': {'type': 'string'},
            'email': {'type': 'string'},
            'estado': {'type': 'integer'}
        }
    }
}
