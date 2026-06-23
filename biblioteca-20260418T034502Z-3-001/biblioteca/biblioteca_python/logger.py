import logging
import logging.config
from datetime import datetime
import os
import copy

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(funcName)s:%(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(__file__), '..', 'logs', 'app.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'delay': True,
            'formatter': 'detailed'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(__file__), '..', 'logs', 'error.log'),
            'maxBytes': 10485760,
            'backupCount': 5,
            'delay': True,
            'formatter': 'detailed'
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(__file__), '..', 'logs', 'audit.log'),
            'maxBytes': 10485760,
            'backupCount': 10,
            'delay': True,
            'formatter': 'detailed'
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False
        },
        'audit': {
            'level': 'INFO',
            'handlers': ['audit_file'],
            'propagate': False
        },
        'flask': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'sqlalchemy': {
            'level': 'WARNING',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    }
}

def setup_logging():
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'logs'), exist_ok=True)
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
    except ValueError as e:
        if "audit_file" not in str(e):
            raise

        fallback_config = copy.deepcopy(LOGGING_CONFIG)
        fallback_config['handlers'].pop('audit_file', None)
        fallback_config['loggers']['audit']['handlers'] = ['console']
        logging.config.dictConfig(fallback_config)
        logging.getLogger('app').warning("audit.log is locked; audit logger fell back to console")

def get_logger(name):
    return logging.getLogger(name)

def get_audit_logger():
    return logging.getLogger('audit')
