# type: ignore
import mysql.connector  # type: ignore
from mysql.connector import pooling, Error  # type: ignore
from config import HOST, USER, PASS, DB, DB_PORT
from logger import get_logger
import threading

logger = get_logger('app')

class DatabasePool:
    """Pool de conexiones MySQL singleton"""

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
                host=HOST,
                user=USER,
                password=PASS,
                database=DB,
                port=DB_PORT,
                charset="utf8mb4",
                autocommit=False,
                raise_on_warnings=False,
            )
            logger.info("Connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing connection pool: {e}")
            raise

    def get_connection(self):
        """Obtener conexión del pool"""
        try:
            return self._pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise

class Query:
    """Gestión de queries con pool de conexiones"""

    def __init__(self):
        self.pool = DatabasePool()
        self.con = None
        try:
            self._get_connection()
        except Exception as e:
            logger.error(f"Failed to get connection in __init__: {e}")
            # No lanzar excepción aquí, dejar que la conexión sea None
            # y que los métodos de query manejen esto

    def _get_connection(self):
        try:
            self.con = self.pool.get_connection()
        except Error as e:
            logger.error(f"Error establishing database connection: {e}")
            self.con = None
            raise

    def _ensure_connection(self):
        """Asegurar que hay una conexión disponible"""
        if self.con is None or not self.con.is_connected():
            self._get_connection()

    def select(self, sql: str, params: tuple = ()):
        """Devuelve una sola fila como dict"""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql, params)
            data = cursor.fetchone()
            # Consumir cualquier resultado pendiente para evitar "Unread result found"
            if data:
                cursor.fetchall()
            return data
        except Error as e:
            logger.error(f"Select error: {sql} - {e}")
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

    def select_all(self, sql: str, params: tuple = ()):
        """Devuelve todas las filas como lista de dicts"""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql, params)
            data = cursor.fetchall()
            return data if data else []
        except Error as e:
            logger.error(f"Select all error: {sql} - {e}")
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

    def save(self, sql: str, params: tuple = ()):
        """Ejecuta INSERT/UPDATE/DELETE, retorna 1 si exitoso o 0"""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            self.con.commit()
            result = 1 if cursor.rowcount > 0 else 0
            return result
        except Error as e:
            if self.con:
                try:
                    self.con.rollback()
                except Exception:
                    pass
            logger.error(f"Save error: {sql} - {e}")
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

    def insert(self, sql: str, params: tuple = ()):
        """INSERT y retorna el lastInsertId, o 0 si falla"""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            self.con.commit()
            last_id = cursor.lastrowid if cursor.rowcount > 0 else 0
            return last_id
        except Error as e:
            if self.con:
                try:
                    self.con.rollback()
                except Exception:
                    pass
            logger.error(f"Insert error: {sql} - {e}")
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

    def transaction(self, callback):
        """Ejecutar operación en transacción"""
        try:
            self._ensure_connection()
            result = callback(self.con)
            self.con.commit()
            return result
        except Error as e:
            self.con.rollback()
            logger.error(f"Transaction error: {e}")
            raise

    def close(self):
        try:
            if self.con and hasattr(self.con, 'is_connected'):
                if self.con.is_connected():
                    self.con.close()
        except Exception:
            pass

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

