from database import Query


class EstudiantesModel(Query):

    def get_estudiantes(self):
        return self.select_all("SELECT * FROM estudiante")

    def insertar_estudiante(self, codigo, dni, nombre, carrera, direccion, telefono):
        existe = self.select("SELECT * FROM estudiante WHERE codigo = %s", (codigo,))
        if not existe:
            sql = ("INSERT INTO estudiante(codigo,dni,nombre,carrera,direccion,telefono) "
                   "VALUES (%s,%s,%s,%s,%s,%s)")
            data = self.save(sql, (codigo, dni, nombre, carrera, direccion, telefono))
            return "ok" if data == 1 else "error"
        return "existe"

    def edit_estudiante(self, id_):
        return self.select("SELECT * FROM estudiante WHERE id = %s", (id_,))

    def actualizar_estudiante(self, codigo, dni, nombre, carrera, direccion, telefono, id_):
        sql = ("UPDATE estudiante SET codigo=%s, dni=%s, nombre=%s, carrera=%s, "
               "direccion=%s, telefono=%s WHERE id=%s")
        data = self.save(sql, (codigo, dni, nombre, carrera, direccion, telefono, id_))
        return "modificado" if data == 1 else "error"

    def estado_estudiante(self, estado, id_):
        return self.save("UPDATE estudiante SET estado=%s WHERE id=%s", (estado, id_))

    def buscar_estudiante(self, valor):
        sql = ("SELECT id, codigo, nombre AS text FROM estudiante "
               "WHERE (codigo LIKE %s AND estado=1) OR (nombre LIKE %s AND estado=1) LIMIT 10")
        return self.select_all(sql, (f"%{valor}%", f"%{valor}%"))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
