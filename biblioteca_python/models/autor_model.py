from database import Query


class AutorModel(Query):

    def get_autor(self):
        return self.select_all("SELECT * FROM autor")

    def insertar_autor(self, autor, img):
        existe = self.select("SELECT * FROM autor WHERE autor = %s", (autor,))
        if not existe:
            data = self.save("INSERT INTO autor(autor, imagen) VALUES (%s, %s)", (autor, img))
            return "ok" if data == 1 else "error"
        return "existe"

    def edit_autor(self, id_):
        return self.select("SELECT * FROM autor WHERE id = %s", (id_,))

    def actualizar_autor(self, autor, img, id_):
        data = self.save("UPDATE autor SET autor=%s, imagen=%s WHERE id=%s", (autor, img, id_))
        return "modificado" if data == 1 else "error"

    def estado_autor(self, estado, id_):
        return self.save("UPDATE autor SET estado=%s WHERE id=%s", (estado, id_))

    def buscar_autor(self, valor):
        sql = "SELECT id, autor AS text FROM autor WHERE autor ILIKE %s AND estado = 1 LIMIT 10"
        return self.select_all(sql, (f"%{valor}%",))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
