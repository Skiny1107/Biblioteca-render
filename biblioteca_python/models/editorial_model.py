from database import Query


class EditorialModel(Query):

    def get_editorial(self):
        return self.select_all("SELECT * FROM editorial")

    def insertar_editorial(self, editorial):
        existe = self.select("SELECT * FROM editorial WHERE editorial = %s", (editorial,))
        if not existe:
            data = self.save("INSERT INTO editorial(editorial) VALUES (%s)", (editorial,))
            return "ok" if data == 1 else "error"
        return "existe"

    def edit_editorial(self, id_):
        return self.select("SELECT * FROM editorial WHERE id = %s", (id_,))

    def actualizar_editorial(self, editorial, id_):
        data = self.save("UPDATE editorial SET editorial=%s WHERE id=%s", (editorial, id_))
        return "modificado" if data == 1 else "error"

    def estado_editorial(self, estado, id_):
        return self.save("UPDATE editorial SET estado=%s WHERE id=%s", (estado, id_))

    def buscar_editorial(self, valor):
        sql = "SELECT id, editorial AS text FROM editorial WHERE editorial ILIKE %s AND estado=1 LIMIT 10"
        return self.select_all(sql, (f"%{valor}%",))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
