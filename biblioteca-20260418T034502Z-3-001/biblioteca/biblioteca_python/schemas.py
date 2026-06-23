from marshmallow import Schema, fields, validate, ValidationError
import re

class UsuarioLoginSchema(Schema):
    usuario = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    clave = fields.Str(required=True, validate=validate.Length(min=8))

class UsuarioRegistroSchema(Schema):
    usuario = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    nombre = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    clave = fields.Str(required=True, validate=validate.Length(min=8))
    confirmar = fields.Str(required=True)

    def validate_usuario_format(self, data, **kwargs):
        if not re.match(r'^[a-zA-Z0-9_-]+$', data['usuario']):
            raise ValidationError('Usuario contiene caracteres inválidos')

class AutorSchema(Schema):
    id = fields.Int(dump_only=True)
    autor = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    imagen = fields.Str(allow_none=True)
    estado = fields.Int(allow_none=True)

class EditorialSchema(Schema):
    id = fields.Int(dump_only=True)
    editorial = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    estado = fields.Int(allow_none=True)

class MateriaSchema(Schema):
    id = fields.Int(dump_only=True)
    materia = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    estado = fields.Int(allow_none=True)

class LibroSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    descripcion = fields.Str(allow_none=True)
    id_autor = fields.Int(required=True)
    id_editorial = fields.Int(required=True)
    isbn = fields.Str(allow_none=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1))
    portada = fields.Str(allow_none=True)
    estado = fields.Int(allow_none=True)

class EstudianteSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    apellido = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    carnet = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    email = fields.Email(allow_none=True)
    telefono = fields.Str(allow_none=True)
    estado = fields.Int(allow_none=True)

class PrestamoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_estudiante = fields.Int(required=True)
    id_libro = fields.Int(required=True)
    fecha_prestamo = fields.DateTime(allow_none=True)
    fecha_devolucion = fields.DateTime(allow_none=True)
    estado = fields.Int(allow_none=True)

class PaginationSchema(Schema):
    page = fields.Int(validate=validate.Range(min=1), missing=1)
    per_page = fields.Int(validate=validate.Range(min=1, max=100), missing=10)
    search = fields.Str(allow_none=True)
