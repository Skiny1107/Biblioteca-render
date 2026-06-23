from database import Query


class MateriaModel(Query):

    def get_materias(self):
        return self.select_all("SELECT * FROM materia")

    def insertar_materia(self, materia):
        existe = self.select("SELECT * FROM materia WHERE materia = %s", (materia,))
        if not existe:
            data = self.save("INSERT INTO materia(materia) VALUES (%s)", (materia,))
            return "ok" if data == 1 else "error"
        return "existe"

    def edit_materia(self, id_):
        return self.select("SELECT * FROM materia WHERE id = %s", (id_,))

    def actualizar_materia(self, materia, id_):
        data = self.save("UPDATE materia SET materia=%s WHERE id=%s", (materia, id_))
        return "modificado" if data == 1 else "error"

    def estado_materia(self, estado, id_):
        return self.save("UPDATE materia SET estado=%s WHERE id=%s", (estado, id_))

    def buscar_materia(self, valor):
        sql = "SELECT id, materia AS text FROM materia WHERE materia ILIKE %s AND estado=1 LIMIT 10"
        return self.select_all(sql, (f"%{valor}%",))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
