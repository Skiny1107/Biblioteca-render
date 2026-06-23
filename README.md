# Sistema de Gestión de Biblioteca - Versión 2.0

Aplicación de gestión de biblioteca en **Python Flask** con arquitectura profesional, seguridad avanzada y DevOps completo.

## ✨ Características Principales

- ✅ **Arquitectura MVC** con separación clara de responsabilidades
- ✅ **Seguridad de nivel profesional** - Hashing de contraseñas, CSRF, Rate limiting
- ✅ **Pool de conexiones BD** - MySQL con pooling para mejor performance
- ✅ **Logging centralizado** - Logs de auditoría, errores y aplicación
- ✅ **Validación robusta** - Marshmallow + Pydantic schemas
- ✅ **API REST** - Endpoints estandarizados con respuestas JSON
- ✅ **Testing** - Tests unitarios e integración con pytest
- ✅ **Dockerización** - Docker + Docker Compose para fácil deployment
- ✅ **CI/CD** - GitHub Actions pipeline automático
- ✅ **Documentación** - Swagger/OpenAPI
- ✅ **Headers de seguridad** - Talisman + CORS
- ✅ **Manejo de errores** - Excepciones personalizadas

## 🚀 Quick Start

### Requisitos Previos
- Python 3.11+
- MySQL 8.0+
- Docker + Docker Compose (opcional)

### Instalación Local

```bash
# 1. Clonar y navegar
cd biblioteca_python

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar ambiente
copy .env.example .env
# Editar .env con tus valores

# 5. Crear logs y uploads
mkdir logs uploads temp

# 6. Ejecutar migraciones
python migrate.py

# 7. Iniciar aplicación
python app.py
```

Acceso: `http://localhost:5000`

### Con Docker

```bash
# Build y start
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Stop
docker-compose down
```

## 📋 Estructura del Proyecto

```
biblioteca/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD Pipeline
├── biblioteca_python/
│   ├── models/                    # Capa de datos
│   ├── routes/                    # Controladores/Endpoints
│   ├── static/                    # CSS, JS, imágenes
│   ├── templates/                 # HTML templates
│   ├── logs/                      # Logs generados
│   ├── app.py                     # App principal
│   ├── config.py                  # Configuración
│   ├── database.py                # Pool de conexiones
│   ├── security.py                # Seguridad y utilidades
│   ├── logger.py                  # Logging
│   ├── exceptions.py              # Excepciones
│   ├── schemas.py                 # Validación
│   ├── services.py                # Lógica de negocio
│   ├── error_handler.py           # Manejo de errores
│   ├── api_response.py            # Respuestas estándar
│   ├── swagger.py                 # Documentación OpenAPI
│   ├── migrate.py                 # Migraciones BD
│   ├── admin.py                   # Herramientas admin
│   ├── requirements.txt           # Dependencias
│   └── .env.example               # Variables de entorno
├── tests/                         # Tests unitarios
├── Dockerfile                     # Docker image
├── docker-compose.yml             # Docker compose
└── DEVELOPMENT.md                 # Guía de desarrollo
```

## 🔐 Seguridad

- **Contraseñas**: Hashing con PBKDF2 (werkzeug.security)
- **CSRF**: Protección contra ataques CSRF
- **Rate Limiting**: Limite de requests por IP (200/día, 50/hora)
- **Headers**: Content Security Policy, HSTS, X-Frame-Options
- **Validación**: Sanitización y validación de entrada
- **Logging**: Auditoría de acciones

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov=biblioteca_python --cov-report=html

# Test específico
pytest tests/test_app.py::test_health_check -v
```

## 📊 Base de Datos

**Tablas principales:**
- `usuarios` - Sistema de usuarios con roles
- `libros` - Catálogo de libros
- `prestamos` - Registro de préstamos
- `estudiantes` - Datos de estudiantes
- `autor`, `editorial`, `materia` - Tablas de referencia

**Pool de conexiones:** 5 conexiones por defecto (configurable)

## 🔧 Variables de Entorno

Ver `.env.example`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-key-here
DB_HOST=localhost
DB_USER=root
DB_PASS=
DB_NAME=biblioteca
```

## 📝 API Endpoints

**Health Check:**
```
GET /health
```

**Usuarios:**
```
GET    /Usuarios/listar          - Listar usuarios
POST   /Usuarios/validar         - Login
POST   /Usuarios/registrar       - Crear/Editar usuario
GET    /Usuarios/editar/<id>     - Obtener usuario
POST   /Usuarios/eliminar/<id>   - Desactivar usuario
POST   /Usuarios/cambiarPas      - Cambiar contraseña
```

**Similar para:** `/Libros`, `/Prestamos`, `/Estudiantes`, etc.

## 🛠️ Herramientas Admin

```bash
python admin.py secrets              # Generar claves secretas
python admin.py admin                # Crear usuario admin
python admin.py reset-password       # Resetear contraseña
python admin.py info                 # Info de BD
```

## 📊 Logs

- `logs/app.log` - Logs generales
- `logs/error.log` - Errores
- `logs/audit.log` - Acciones de usuarios
- `logs/access.log` - Requests HTTP (producción)

## 🚢 Deployment

**Production:**
```bash
# Con gunicorn
gunicorn -c gunicorn_config.py app:app

# Con nginx + gunicorn (recomendado)
# Ver DEVELOPMENT.md
```

## 🔄 CI/CD

GitHub Actions ejecuta automáticamente:
- Linting (flake8)
- Tests (pytest)
- Coverage reports
- Docker build y push

## 📈 Performance

- Connection pooling
- Paginación automática
- Caché potencial con Redis
- Compresión GZIP
- Índices de BD

## 🤝 Contribuir

1. Crear rama: `git checkout -b feature/mi-feature`
2. Commit: `git commit -am 'Add feature'`
3. Push: `git push origin feature/mi-feature`
4. Pull request

## 📞 Soporte

Para reportar issues o sugerencias, crear un issue en GitHub.

## 📄 Licencia

MIT License

---

**Versión:** 2.0.0
**Última actualización:** 2024

