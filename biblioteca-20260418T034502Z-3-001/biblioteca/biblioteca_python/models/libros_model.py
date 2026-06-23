from database import Query


class LibrosModel(Query):

    def get_libros(self):
        sql = ("SELECT l.*, m.materia, a.autor, e.editorial "
               "FROM libro l "
               "INNER JOIN materia m ON l.id_materia = m.id "
               "INNER JOIN autor a ON l.id_autor = a.id "
               "INNER JOIN editorial e ON l.id_editorial = e.id")
        return self.select_all(sql)

    def insertar_libros(self, titulo, id_autor, id_editorial, id_materia,
                        cantidad, num_pagina, anio_edicion, descripcion, img_nombre):
        existe = self.select("SELECT * FROM libro WHERE titulo = %s", (titulo,))
        if not existe:
            sql = ("INSERT INTO libro(titulo, id_autor, id_editorial, id_materia, "
                   "cantidad, num_pagina, anio_edicion, descripcion, imagen) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            data = self.save(sql, (titulo, id_autor, id_editorial, id_materia,
                                   cantidad, num_pagina, anio_edicion, descripcion, img_nombre))
            return "ok" if data == 1 else "error"
        return "existe"

    def edit_libros(self, id_):
        sql = "SELECT * FROM libro WHERE id = %s"
        return self.select(sql, (id_,))

    def actualizar_libros(self, titulo, id_autor, id_editorial, id_materia,
                          cantidad, num_pagina, anio_edicion, descripcion, img_nombre, id_):
        sql = ("UPDATE libro SET titulo=%s, id_autor=%s, id_editorial=%s, id_materia=%s, "
               "cantidad=%s, num_pagina=%s, anio_edicion=%s, descripcion=%s, imagen=%s WHERE id=%s")
        data = self.save(sql, (titulo, id_autor, id_editorial, id_materia,
                               cantidad, num_pagina, anio_edicion, descripcion, img_nombre, id_))
        return "modificado" if data == 1 else "error"

    def estado_libros(self, estado, id_):
        sql = "UPDATE libro SET estado = %s WHERE id = %s"
        return self.save(sql, (estado, id_))

    def buscar_libro(self, valor):
        sql = "SELECT id, titulo AS text FROM libro WHERE titulo LIKE %s AND estado = 1 LIMIT 10"
        return self.select_all(sql, (f"%{valor}%",))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))
