import multiprocessing
import os

# ── Puerto ─────────────────────────────────────────────────────────────────
# Render inyecta $PORT; en local se usa 5000
port = os.getenv('PORT', '5000')
bind = f"0.0.0.0:{port}"

# ── Workers ────────────────────────────────────────────────────────────────
# En Render free tier: 2 workers máximo; localmente usamos más
_cpu = multiprocessing.cpu_count()
workers = 2 if os.getenv('RENDER') else (_cpu * 2 + 1)
worker_class = 'sync'
max_requests = 1000
max_requests_jitter = 50
timeout = 120
graceful_timeout = 30
keepalive = 5

# ── Logging → stdout/stderr (requerido por Render) ────────────────────────
# No se escriben archivos de log; Render captura stdout/stderr directamente
accesslog = '-'   # '-' = stdout
errorlog = '-'    # '-' = stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s'

# ── Proceso ────────────────────────────────────────────────────────────────
daemon = False
pidfile = None


def on_starting(server):
    import logging
    logging.getLogger('gunicorn.error').info('Gunicorn starting…')


def when_ready(server):
    import logging
    logging.getLogger('gunicorn.error').info(f'Server ready on port {port}')
