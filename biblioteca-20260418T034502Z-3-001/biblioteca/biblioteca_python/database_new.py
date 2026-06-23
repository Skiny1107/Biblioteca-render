import mysql.connector
from mysql.connector import pooling, Error
from config import config as cfg
from logger import get_logger
import threading

logger = get_logger('app')

class DatabasePool:
    """Pool de conexiones MySQL con conexión segura"""

    _instance = None
    _lock = threading.Lock()
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabasePool, cls).__new__(cls)
                    cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        try:
            self._pool = pooling.MySQLConnectionPool(
                pool_name="biblioteca_pool",
                pool_size=5,
                pool_reset_session=True,
                host=cfg.DB_HOST,
                user=cfg.DB_USER,
                password=cfg.DB_PASS,
                database=cfg.DB_NAME,
                port=cfg.DB_PORT,
                charset="utf8mb4",
                autocommit=False,
                raise_on_warnings=False,
            )
            logger.info("Connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing connection pool: {e}")
            raise

    def get_connection(self):
        """Obtener una conexión del pool"""
        try:
            return self._pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise

class DatabaseContext:
    """Context manager para manejo de conexiones"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        pool = DatabasePool()
        self.connection = pool.get_connection()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

        if exc_type is not None:
            logger.error(f"Database error: {exc_type.__name__} - {exc_val}")
            return False
        return True

class Query:
    """Equivalente mejorado de Conexion + Query de PHP"""

    def __init__(self):
        self.pool = DatabasePool()
        self.con = None
        self._get_connection()

    def _get_connection(self):
        try:
            self.con = self.pool.get_connection()
        except Error as e:
            logger.error(f"Error establishing database connection: {e}")
            raise

    def select(self, sql: str, params: tuple = ()):
        """Devuelve una sola fila como dict"""
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql, params)
            data = cursor.fetchone()
            return data
        except Error as e:
            logger.error(f"Select error: {sql} - {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def select_all(self, sql: str, params: tuple = ()):
        """Devuelve todas las filas como lista de dicts"""
        cursor = None
        try:
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql, params)
            data = cursor.fetchall()
            return data if data else []
        except Error as e:
            logger.error(f"Select all error: {sql} - {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def save(self, sql: str, params: tuple = ()):
        """Ejecuta INSERT/UPDATE/DELETE, retorna 1 si exitoso o 0"""
        cursor = None
        try:
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            self.con.commit()
            result = 1 if cursor.rowcount > 0 else 0
            return result
        except Error as e:
            self.con.rollback()
            logger.error(f"Save error: {sql} - {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def insert(self, sql: str, params: tuple = ()):
        """INSERT y retorna el lastInsertId, o 0 si falla"""
        cursor = None
        try:
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            self.con.commit()
            last_id = cursor.lastrowid if cursor.rowcount > 0 else 0
            return last_id
        except Error as e:
            self.con.rollback()
            logger.error(f"Insert error: {sql} - {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def transaction(self, callback):
        """Ejecutar en transacción"""
        try:
            result = callback(self.con)
            self.con.commit()
            return result
        except Error as e:
            self.con.rollback()
            logger.error(f"Transaction error: {e}")
            raise

    def close(self):
        if self.con and self.con.is_connected():
            self.con.close()

    def __del__(self):
        self.close()
