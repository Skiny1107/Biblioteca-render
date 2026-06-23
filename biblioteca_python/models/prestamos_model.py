from database import Query


class PrestamosModel(Query):

    def get_prestamos(self, estado=None, fecha_desde=None, fecha_hasta=None):
        sql = (
            "SELECT e.id AS est_id, e.nombre AS est_nombre, "
            "l.id AS lib_id, l.titulo, "
            "p.id AS pres_id, p.id_estudiante, p.id_libro, "
            "p.fecha_prestamo, p.fecha_devolucion, p.cantidad, p.observacion, p.estado "
            "FROM prestamo p "
            "INNER JOIN estudiante e ON p.id_estudiante = e.id "
            "INNER JOIN libro l ON p.id_libro = l.id "
            "WHERE 1=1"
        )
        condiciones = []
        valores = []
        if estado is not None and estado != '':
            condiciones.append("p.estado = %s")
            valores.append(int(estado))
        if fecha_desde:
            condiciones.append("p.fecha_prestamo >= %s")
            valores.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("p.fecha_prestamo <= %s")
            valores.append(fecha_hasta)
        if condiciones:
            sql += " AND " + " AND ".join(condiciones)
        sql += " ORDER BY p.id DESC"
        return self.select_all(sql, tuple(valores)) if valores else self.select_all(sql)

    def insertar_prestamo(self, estudiante, libro, cantidad,
                          fecha_prestamo, fecha_devolucion, observacion, estado_inicial=1):
        try:
            cantidad_int = int(cantidad)
            if cantidad_int <= 0:
                return "cantidad_invalida"
        except (TypeError, ValueError):
            return "cantidad_invalida"

        # Validamos si ya existe uno activo (estado 1) o pendiente (estado 2)
        existe = self.select(
            "SELECT * FROM prestamo WHERE id_libro = %s AND id_estudiante = %s AND (estado = 1 OR estado = 2)",
            (libro, estudiante)
        )
        if not existe:
            libro_row = self.select("SELECT * FROM libro WHERE id = %s", (libro,))
            if not libro_row:
                return "libro_no_encontrado"
            if libro_row['cantidad'] < cantidad_int:
                return "sin_stock"

            sql = ("INSERT INTO prestamo(id_estudiante, id_libro, fecha_prestamo, "
                   "fecha_devolucion, cantidad, observacion, estado) VALUES (%s,%s,%s,%s,%s,%s,%s)")
            data = self.insert(sql, (estudiante, libro, fecha_prestamo,
                                     fecha_devolucion, cantidad_int, observacion, estado_inicial))
            if data > 0:
                # Si el estado inicial es 1 (Admin aprueba directo o crea), restamos stock
                if estado_inicial == 1:
                    total = libro_row['cantidad'] - cantidad_int
                    self.save("UPDATE libro SET cantidad = %s WHERE id = %s", (total, libro))
                return data
            return 0
        return "existe"

    def aprobar_prestamo(self, id_):
        prestamo = self.select("SELECT * FROM prestamo WHERE id = %s AND estado = 2", (id_,))
        if prestamo:
            libro_row = self.select("SELECT * FROM libro WHERE id = %s", (prestamo['id_libro'],))
            if libro_row and libro_row['cantidad'] >= prestamo['cantidad']:
                sql = "UPDATE prestamo SET estado = 1 WHERE id = %s"
                data = self.save(sql, (id_,))
                if data == 1:
                    total = libro_row['cantidad'] - prestamo['cantidad']
                    self.save("UPDATE libro SET cantidad = %s WHERE id = %s", (total, prestamo['id_libro']))
                    return "ok"
            else:
                return "sin_stock"
        return "error"
        
    def rechazar_prestamo(self, id_):
        sql = "UPDATE prestamo SET estado = 3 WHERE id = %s AND estado = 2"
        data = self.save(sql, (id_,))
        if data == 1:
            return "ok"
        return "error"

    def actualizar_prestamo(self, estado, id_):
        sql = "UPDATE prestamo SET estado = %s WHERE id = %s"
        data = self.save(sql, (estado, id_))
        if data == 1:
            prestamo = self.select("SELECT * FROM prestamo WHERE id = %s", (id_,))
            libro = self.select("SELECT * FROM libro WHERE id = %s", (prestamo['id_libro'],))
            total = libro['cantidad'] + prestamo['cantidad']
            self.save("UPDATE libro SET cantidad = %s WHERE id = %s",
                      (total, prestamo['id_libro']))
            return "ok"
        return "error"

    def select_datos(self):
        return self.select("SELECT * FROM configuracion")

    def get_cant_libro(self, libro):
        return self.select("SELECT * FROM libro WHERE id = %s", (libro,))

    def select_prestamo_debe(self):
        sql = (
            "SELECT e.id AS est_id, e.nombre AS est_nombre, "
            "l.id AS lib_id, l.titulo, "
            "p.id AS pres_id, p.id_estudiante, p.id_libro, "
            "p.fecha_prestamo, p.fecha_devolucion, p.cantidad, p.observacion, p.estado "
            "FROM prestamo p "
            "INNER JOIN estudiante e ON p.id_estudiante = e.id "
            "INNER JOIN libro l ON p.id_libro = l.id "
            "WHERE p.estado = 1 ORDER BY e.nombre ASC"
        )
        return self.select_all(sql)

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))

    def get_prestamo_libro(self, id_prestamo):
        sql = (
            "SELECT e.id AS est_id, e.codigo, e.nombre AS est_nombre, e.carrera, "
            "l.id AS lib_id, l.titulo, "
            "p.id AS pres_id, p.id_estudiante, p.id_libro, "
            "p.fecha_prestamo, p.fecha_devolucion, p.cantidad, p.observacion, p.estado "
            "FROM prestamo p "
            "INNER JOIN estudiante e ON p.id_estudiante = e.id "
            "INNER JOIN libro l ON p.id_libro = l.id "
            "WHERE p.id = %s"
        )
        return self.select(sql, (id_prestamo,))
