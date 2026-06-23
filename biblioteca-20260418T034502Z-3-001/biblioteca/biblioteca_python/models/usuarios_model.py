from database import Query
from security import SecurityUtils
from logger import get_logger

logger = get_logger('app')


class UsuariosModel(Query):

    def get_usuario(self, usuario, clave):
        try:
            sql = "SELECT * FROM usuarios WHERE usuario = %s AND estado = 1 ORDER BY id DESC"
            results = self.select_all(sql, (usuario,))
            for result in results:
                if SecurityUtils.verify_password(clave, result.get('clave', '')):
                    return result
            return None
        except Exception as e:
            logger.error(f"Error in get_usuario: {e}")
            raise

    def get_usuarios(self):
        try:
            sql = "SELECT id, usuario, nombre, estado FROM usuarios"
            return self.select_all(sql)
        except Exception as e:
            logger.error(f"Error in get_usuarios: {e}")
            raise

    def registrar_usuario(self, usuario, nombre, clave):
        try:
            existe = self.select("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
            if existe:
                return "existe"

            hash_clave = SecurityUtils.hash_password(clave)
            sql = "INSERT INTO usuarios(usuario, nombre, clave) VALUES (%s, %s, %s)"
            data = self.save(sql, (usuario, nombre, hash_clave))
            return "ok" if data == 1 else "error"
        except Exception as e:
            logger.error(f"Error in registrar_usuario: {e}")
            raise

    def modificar_usuario(self, usuario, nombre, id_):
        try:
            existe = self.select("SELECT id FROM usuarios WHERE usuario = %s AND id != %s", (usuario, id_))
            if existe:
                return "existe"
            sql = "UPDATE usuarios SET usuario = %s, nombre = %s WHERE id = %s"
            data = self.save(sql, (usuario, nombre, id_))
            return "modificado" if data == 1 else "error"
        except Exception as e:
            logger.error(f"Error in modificar_usuario: {e}")
            raise

    def editar_user(self, id_):
        try:
            sql = "SELECT id, usuario, nombre, estado FROM usuarios WHERE id = %s"
            return self.select(sql, (id_,))
        except Exception as e:
            logger.error(f"Error in editar_user: {e}")
            raise

    def accion_user(self, estado, id_):
        try:
            sql = "UPDATE usuarios SET estado = %s WHERE id = %s"
            return self.save(sql, (estado, id_))
        except Exception as e:
            logger.error(f"Error in accion_user: {e}")
            raise

    def get_permisos(self):
        try:
            sql = "SELECT * FROM permisos"
            return self.select_all(sql)
        except Exception as e:
            logger.error(f"Error in get_permisos: {e}")
            raise

    def get_permisos_usuario(self, id_):
        try:
            sql = ("SELECT p.nombre FROM permisos p "
                   "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
                   "WHERE d.id_usuario = %s")
            return self.select_all(sql, (id_,))
        except Exception as e:
            logger.error(f"Error in get_permisos_usuario: {e}")
            raise

    def get_detalle_permisos(self, id_):
        try:
            sql = "SELECT * FROM detalle_permisos WHERE id_usuario = %s"
            return self.select_all(sql, (id_,))
        except Exception as e:
            logger.error(f"Error in get_detalle_permisos: {e}")
            raise

    def delete_permisos(self, id_):
        try:
            sql = "DELETE FROM detalle_permisos WHERE id_usuario = %s"
            return self.save(sql, (id_,))
        except Exception as e:
            logger.error(f"Error in delete_permisos: {e}")
            raise

    def actualizar_permisos(self, usuario, permiso):
        try:
            sql = "INSERT INTO detalle_permisos(id_usuario, id_permiso) VALUES (%s, %s)"
            data = self.save(sql, (usuario, permiso))
            return "ok" if data == 1 else "error"
        except Exception as e:
            logger.error(f"Error in actualizar_permisos: {e}")
            raise

    def verificar_permisos(self, id_user, permiso):
        try:
            sql = ("SELECT p.*, d.* FROM permisos p "
                   "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
                   "WHERE d.id_usuario = %s AND p.nombre = %s")
            existe = self.select(sql, (id_user, permiso))
            return bool(existe)
        except Exception as e:
            logger.error(f"Error in verificar_permisos: {e}")
            return False

    def actualizar_pass(self, clave, id_):
        try:
            hash_clave = SecurityUtils.hash_password(clave)
            sql = "UPDATE usuarios SET clave = %s WHERE id = %s"
            data = self.save(sql, (hash_clave, id_))
            return "modificado" if data == 1 else "error"
        except Exception as e:
            logger.error(f"Error in actualizar_pass: {e}")
            raise
