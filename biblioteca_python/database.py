import os
import threading
import psycopg2
import psycopg2.pool
import psycopg2.extras
from config import config as cfg
from logger import get_logger

logger = get_logger('app')


def _build_dsn() -> str:
    """Construir DSN de PostgreSQL desde DATABASE_URL o variables individuales."""
    url = os.getenv('DATABASE_URL', '')
    if url:
        # Render entrega 'postgres://...' — psycopg2 necesita 'postgresql://'
        if url.startswith('postgres://'):
            url = 'postgresql://' + url[len('postgres://'):]
        return url
    return (
        f"host={cfg.DB_HOST} port={cfg.DB_PORT} "
        f"dbname={cfg.DB_NAME} user={cfg.DB_USER} password={cfg.DB_PASS} "
        "sslmode=prefer connect_timeout=10"
    )


class DatabasePool:
    """Pool de conexiones PostgreSQL singleton thread-safe."""

    _instance = None
    _lock = threading.Lock()
    _pool: psycopg2.pool.ThreadedConnectionPool | None = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    try:
                        instance = super().__new__(cls)
                        instance._initialize_pool()
                        cls._instance = instance
                    except Exception:
                        cls._instance = None
                        raise
        return cls._instance

    def _initialize_pool(self):
        dsn = _build_dsn()
        self._pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=dsn,
        )
        logger.info("PostgreSQL connection pool initialized")

    def get_connection(self):
        try:
            return self._pool.getconn()
        except psycopg2.pool.PoolError as e:
            logger.error(f"Pool exhausted: {e}")
            raise

    def return_connection(self, conn):
        try:
            if conn:
                self._pool.putconn(conn)
        except Exception:
            pass

    def close_all(self):
        if self._pool:
            self._pool.closeall()


class Query:
    """Capa de acceso a datos con PostgreSQL — mantiene la misma API que la versión MySQL."""

    def __init__(self):
        self._pool_manager = DatabasePool()
        self.con = None
        self._get_connection()

    def _get_connection(self):
        try:
            self.con = self._pool_manager.get_connection()
            self.con.set_client_encoding('UTF8')
            self.con.autocommit = False
        except Exception as e:
            logger.error(f"Error getting DB connection: {e}")
            self.con = None
            raise

    def _ensure_connection(self):
        """Reconectar si la conexión fue cerrada o expiró."""
        if self.con is None or self.con.closed:
            self._get_connection()

    # ─── Helpers internos ────────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(cursor, row) -> dict:
        """Convertir fila a dict usando los nombres de columna del cursor."""
        if row is None:
            return None
        cols = [desc[0] for desc in cursor.description]
        return dict(zip(cols, row))

    # ─── API pública ─────────────────────────────────────────────────────────

    def select(self, sql: str, params: tuple = ()) -> dict | None:
        """Devuelve una sola fila como dict, o None."""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return self._row_to_dict(cursor, row)
        except psycopg2.Error as e:
            logger.error(f"Select error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def select_all(self, sql: str, params: tuple = ()) -> list:
        """Devuelve todas las filas como lista de dicts."""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if not rows:
                return []
            cols = [desc[0] for desc in cursor.description]
            return [dict(zip(cols, row)) for row in rows]
        except psycopg2.Error as e:
            logger.error(f"Select all error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def save(self, sql: str, params: tuple = ()) -> int:
        """Ejecuta INSERT/UPDATE/DELETE. Devuelve 1 si afectó filas, 0 si no."""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            self.con.commit()
            return 1 if cursor.rowcount > 0 else 0
        except psycopg2.Error as e:
            if self.con:
                self.con.rollback()
            logger.error(f"Save error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def insert(self, sql: str, params: tuple = ()) -> int:
        """INSERT con RETURNING id. Devuelve el nuevo ID o 0."""
        cursor = None
        try:
            self._ensure_connection()
            cursor = self.con.cursor()
            # Añadir RETURNING id si la query no lo incluye ya
            returning_sql = sql
            if 'RETURNING' not in sql.upper():
                returning_sql = sql.rstrip(';') + ' RETURNING id'
            cursor.execute(returning_sql, params)
            self.con.commit()
            row = cursor.fetchone()
            return row[0] if row else 0
        except psycopg2.Error as e:
            if self.con:
                self.con.rollback()
            logger.error(f"Insert error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def transaction(self, callback):
        """Ejecutar operación en transacción explícita."""
        try:
            self._ensure_connection()
            result = callback(self.con)
            self.con.commit()
            return result
        except psycopg2.Error as e:
            if self.con:
                self.con.rollback()
            logger.error(f"Transaction error: {e}")
            raise

    def close(self):
        """Devolver la conexión al pool."""
        try:
            if self.con and not self.con.closed:
                self._pool_manager.return_connection(self.con)
                self.con = None
        except Exception:
            pass

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
