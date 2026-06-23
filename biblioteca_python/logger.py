import logging
import logging.config
import os
import copy

# En producción (Render) solo console; en desarrollo también archivos
_IS_PROD = os.getenv('FLASK_ENV', 'development') == 'production'

_handlers_base = {
    'console': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'standard',
    },
}

if not _IS_PROD:
    _logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(_logs_dir, exist_ok=True)
    _handlers_base.update({
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(_logs_dir, 'app.log'),
            'maxBytes': 10_485_760,
            'backupCount': 5,
            'delay': True,
            'formatter': 'detailed',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(_logs_dir, 'error.log'),
            'maxBytes': 10_485_760,
            'backupCount': 5,
            'delay': True,
            'formatter': 'detailed',
        },
    })

_app_handlers = ['console'] if _IS_PROD else ['console', 'file', 'error_file']

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(funcName)s:%(lineno)d - %(message)s',
        },
    },
    'handlers': _handlers_base,
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': _app_handlers,
            'propagate': False,
        },
        'flask': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


def setup_logging():
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('app').warning(f"Logging setup fallback: {e}")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def get_audit_logger() -> logging.Logger:
    return logging.getLogger('app')
