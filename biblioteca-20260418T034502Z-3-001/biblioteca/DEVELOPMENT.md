# Configuración para desarrolladores

## Setup Inicial

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r biblioteca_python/requirements.txt

# 4. Copiar .env
copy biblioteca_python\.env.example biblioteca_python\.env

# 5. Configurar variables en .env
# Editar: DB_HOST, DB_USER, DB_PASS, SECRET_KEY, JWT_SECRET

# 6. Crear directorios necesarios
mkdir logs uploads temp
```

## Ejecución

```bash
# Desarrollo
python -m flask run

# O directamente
cd biblioteca_python
python app.py

# Production con gunicorn
gunicorn -c gunicorn_config.py app:app
```

## Testing

```bash
# Ejecutar tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=biblioteca_python --cov-report=html

# Test específico
pytest tests/test_app.py::test_health_check -v
```

## Docker

```bash
# Build
docker-compose build

# Up
docker-compose up -d

# Down
docker-compose down

# Logs
docker-compose logs -f app

# Acceder a la app
# http://localhost:5000
# http://localhost:5000/health (health check)
```

## Base de datos

```bash
# Restaurar dump
mysql -u root -p biblioteca < biblioteca.sql

# Dentro de docker
docker-compose exec mysql mysql -u root -proot biblioteca < biblioteca.sql
```

## API Endpoints

- Health: `GET /health`
- Swagger: `GET /apidocs` (cuando esté en producción)
- Usuarios: `/Usuarios/*`
- Libros: `/Libros/*`
- Prestamos: `/Prestamos/*`
- Estudiantes: `/Estudiantes/*`
- etc...

## Logs

Los logs se guardan en:
- `logs/app.log` - Logs generales
- `logs/error.log` - Errores
- `logs/audit.log` - Auditoría (acciones de usuarios)

## Seguridad

- Todas las contraseñas se hashean con werkzeug
- CSRF protection habilitada
- Rate limiting activo (200 requests/día, 50/hora)
- Headers de seguridad (Talisman)
- Validación de entrada (marshmallow)
- JWT tokens para API

## Estructura de proyecto

```
biblioteca/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD Pipeline
├── biblioteca_python/
│   ├── models/                 # Modelos (logica datos)
│   ├── routes/                 # Rutas/Controladores
│   ├── static/                 # Archivos estáticos (CSS, JS, imgs)
│   ├── templates/              # HTML templates
│   ├── logs/                   # Logs generados
│   ├── app.py                  # App principal
│   ├── config.py               # Configuración
│   ├── database.py             # Pool de conexiones
│   ├── security.py             # Utilidades de seguridad
│   ├── logger.py               # Logging centralizado
│   ├── exceptions.py           # Excepciones personalizadas
│   ├── schemas.py              # Validación de datos
│   ├── services.py             # Servicios (logica negocio)
│   ├── error_handler.py        # Manejo de errores
│   ├── api_response.py         # Respuestas API estandarizadas
│   ├── swagger.py              # Documentación Swagger
│   ├── gunicorn_config.py      # Config de gunicorn
│   ├── requirements.txt        # Dependencias
│   └── .env.example            # Variables de entorno
├── tests/                      # Tests
├── docker-compose.yml          # Docker compose
├── Dockerfile                  # Docker image
└── README.md                   # Documentación
```

## Performance Tips

1. Usar caché de Redis para consultas frecuentes
2. Paginar resultados (máximo 100 items)
3. Crear índices en BD para búsquedas
4. Usar connection pool (ya implementado)
5. Comprimir respuestas (GZIP)

## Deploying a Producción

1. Cambiar `FLASK_ENV=production` en .env
2. Generar `SECRET_KEY` y `JWT_SECRET` seguros
3. Configurar `SESSION_COOKIE_SECURE=True`
4. Usar gunicorn en lugar de Flask dev server
5. Poner detrás de nginx/apache
6. Habilitar HTTPS/SSL
7. Configurar backup de BD
8. Monitorear logs y errors
