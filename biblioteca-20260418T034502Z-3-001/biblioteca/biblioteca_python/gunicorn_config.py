import multiprocessing
import os

# Servidor
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = os.path.join(os.path.dirname(__file__), '..', 'logs', 'access.log')
errorlog = os.path.join(os.path.dirname(__file__), '..', 'logs', 'error.log')
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Seguridad
limit_concurrency = 500
limit_max_requests = 10000

# Procesos
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Hooks
def on_starting(server):
    import logging
    logger = logging.getLogger('gunicorn.glogging')
    logger.info('Starting Gunicorn server')

def when_ready(server):
    import logging
    logger = logging.getLogger('gunicorn.glogging')
    logger.info('Server is ready. Spawning workers')

def on_exit(server):
    import logging
    logger = logging.getLogger('gunicorn.glogging')
    logger.info('Server shutting down')
