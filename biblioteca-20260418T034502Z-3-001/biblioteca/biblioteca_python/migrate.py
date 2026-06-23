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
                    'ALTER TABLE usuarios ADD INDEX idx_usuario (usuario);',
                    'ALTER TABLE usuarios ADD INDEX idx_estado (estado);',
                    'ALTER TABLE libro ADD INDEX idx_titulo (titulo(191));',
                    'ALTER TABLE estudiante ADD INDEX idx_codigo (codigo);',
                    'ALTER TABLE estudiante ADD INDEX idx_estado (estado);',
                    'ALTER TABLE prestamo ADD INDEX idx_estudiante (id_estudiante);',
                    'ALTER TABLE prestamo ADD INDEX idx_libro (id_libro);',
                    'ALTER TABLE prestamo ADD INDEX idx_estado (estado);',
                ]
            },
            {
                'version': '1.1',
                'description': 'Add audit columns',
                'sql': [
                    'ALTER TABLE usuarios ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;',
                    'ALTER TABLE usuarios ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;',
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
