from database import Query


class ConfiguracionModel(Query):

    def select_configuracion(self):
        return self.select("SELECT * FROM configuracion")

    def actualizar_config(self, nombre, telefono, direccion, correo, img, id_):
        sql = ("UPDATE configuracion SET nombre=%s, telefono=%s, direccion=%s, "
               "correo=%s, foto=%s WHERE id=%s")
        data = self.save(sql, (nombre, telefono, direccion, correo, img, id_))
        return "modificado" if data == 1 else "error"

    def select_datos(self, tabla):
        sql = f"SELECT COUNT(*) AS total FROM {tabla} WHERE estado = 1"
        return self.select(sql)

    def get_reportes(self):
        return self.select_all("SELECT titulo, cantidad FROM libro WHERE estado = 1")

    def get_verificar_prestamos(self, date):
        sql = ("SELECT p.id, p.id_estudiante, p.fecha_prestamo, p.fecha_devolucion, "
               "p.cantidad, p.estado, e.id AS est_id, e.nombre AS est_nombre, "
               "l.id AS lib_id, l.titulo "
               "FROM prestamo p "
               "INNER JOIN estudiante e ON p.id_estudiante = e.id "
               "INNER JOIN libro l ON p.id_libro = l.id "
               "WHERE p.fecha_devolucion < %s AND p.estado = 1")
        return self.select_all(sql, (date,))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
