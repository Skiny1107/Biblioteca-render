#!/usr/bin/env python
"""
Script para ejecutar la aplicación sin reloader (para desarrollo)
"""
import sys
import os

# Agregar la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from biblioteca_python.app import app
from biblioteca_python.config import config as cfg
from biblioteca_python.logger import get_logger

logger = get_logger('app')

if __name__ == '__main__':
    logger.info(f"Starting Biblioteca application (NO RELOADER)")

    # Ejecutar sin reloader
    app.run(
        debug=False,
        port=5000,
        host='0.0.0.0',
        use_reloader=False  # IMPORTANTE: Sin reloader
    )
