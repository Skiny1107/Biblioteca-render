#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Query
from logger import setup_logging, get_logger

setup_logging()
logger = get_logger('app')

class DatabaseMigrator:
    """Herramienta de migraciones de BD"""

    def __init__(self):
        self.migrations = [
            {
                'version': '1.0',
                'description': 'Add indexes to improve performance',
                'sql': [
                    'CREATE INDEX idx_usuario ON usuarios (usuario);',
                    'CREATE INDEX idx_estado ON usuarios (estado);',
                    'CREATE INDEX idx_titulo ON libro (titulo);',
                    'CREATE INDEX idx_codigo ON estudiante (codigo);',
                    'CREATE INDEX idx_estado_estudiante ON estudiante (estado);',
                    'CREATE INDEX idx_estudiante ON prestamo (id_estudiante);',
                    'CREATE INDEX idx_libro ON prestamo (id_libro);',
                    'CREATE INDEX idx_estado_prestamo ON prestamo (estado);',
                ]
            },
            {
                'version': '1.1',
                'description': 'Add audit columns',
                'sql': [
                    'ALTER TABLE usuarios ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;',
                    'ALTER TABLE usuarios ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;',
                ]
            }
        ]

    def run_migration(self, sql_list):
        """Ejecutar una migración"""
        try:
            db = Query()
            for sql in sql_list:
                if sql.strip():
                    try:
                        db.save(sql)
                        logger.info(f"Executed: {sql[:50]}...")
                    except Exception as e:
                        logger.warning(f"Skipped (already exists): {sql[:50]}... - {e}")
            db.close()
            return True
        except Exception as e:
            logger.error(f"Migration error: {e}")
            return False

    def run_all(self):
        """Ejecutar todas las migraciones"""
        logger.info("Starting database migrations...")
        for migration in self.migrations:
            logger.info(f"Running migration {migration['version']}: {migration['description']}")
            if self.run_migration(migration['sql']):
                logger.info(f"Migration {migration['version']} completed successfully")
            else:
                logger.error(f"Migration {migration['version']} failed")
        logger.info("All migrations completed")

if __name__ == '__main__':
    migrator = DatabaseMigrator()
    migrator.run_all()
