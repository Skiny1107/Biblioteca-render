from database import Query


class LibrosModel(Query):

    def get_libros(self, id_autor=None, id_editorial=None, id_materia=None, estado=None, q=None):
        sql = ("SELECT l.*, m.materia, a.autor, e.editorial "
               "FROM libro l "
               "INNER JOIN materia m ON l.id_materia = m.id "
               "INNER JOIN autor a ON l.id_autor = a.id "
               "INNER JOIN editorial e ON l.id_editorial = e.id")
        
        condiciones = []
        valores = []
        
        if id_autor:
            condiciones.append("l.id_autor = %s")
            valores.append(id_autor)
        if id_editorial:
            condiciones.append("l.id_editorial = %s")
            valores.append(id_editorial)
        if id_materia:
            condiciones.append("l.id_materia = %s")
            valores.append(id_materia)
        if estado is not None and estado != '':
            condiciones.append("l.estado = %s")
            valores.append(int(estado))
        if q:
            condiciones.append("(l.titulo ILIKE %s OR a.autor ILIKE %s OR m.materia ILIKE %s OR e.editorial ILIKE %s)")
            term = f"%{q}%"
            valores.extend([term, term, term, term])
            
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)
            
        res = self.select_all(sql, tuple(valores)) if valores else self.select_all(sql)
        for r in res:
            if isinstance(r, dict) and 'isbn' not in r:
                r['isbn'] = '978-3-16-148410-0'
        return res

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
        sql = ("SELECT l.id, CONCAT(l.titulo, ' - ', a.autor, ' [', e.editorial, ']') AS text "
               "FROM libro l "
               "INNER JOIN autor a ON l.id_autor = a.id "
               "INNER JOIN editorial e ON l.id_editorial = e.id "
               "WHERE (l.titulo ILIKE %s OR a.autor ILIKE %s OR e.editorial ILIKE %s) "
               "AND l.estado = 1 LIMIT 10")
        term = f"%{valor}%"
        return self.select_all(sql, (term, term, term))

    def verificar_permisos(self, id_user, permiso):
        sql = ("SELECT p.*, d.* FROM permisos p "
               "INNER JOIN detalle_permisos d ON p.id = d.id_permiso "
               "WHERE d.id_usuario = %s AND p.nombre = %s")
        return bool(self.select(sql, (id_user, permiso)))

    # ─── Métodos para carga masiva ───────────────────────────────────────────

    def get_or_create_autor(self, nombre: str) -> int:
        """Devuelve el id del autor existente o lo crea y devuelve el nuevo id."""
        row = self.select("SELECT id FROM autor WHERE autor = %s", (nombre,))
        if row:
            return row['id']
        return self.insert("INSERT INTO autor(autor, imagen) VALUES (%s, %s)", (nombre, 'logo.png'))

    def get_or_create_editorial(self, nombre: str) -> int:
        """Devuelve el id de la editorial existente o la crea."""
        row = self.select("SELECT id FROM editorial WHERE editorial = %s", (nombre,))
        if row:
            return row['id']
        return self.insert("INSERT INTO editorial(editorial) VALUES (%s)", (nombre,))

    def get_or_create_materia(self, nombre: str) -> int:
        """Devuelve el id de la materia existente o la crea."""
        row = self.select("SELECT id FROM materia WHERE materia = %s", (nombre,))
        if row:
            return row['id']
        return self.insert("INSERT INTO materia(materia) VALUES (%s)", (nombre,))

    def insertar_o_sumar_libro(self, titulo, id_autor, id_editorial, id_materia,
                               cantidad, num_pagina, anio_edicion, descripcion):
        """
        Si el libro no existe lo inserta; si ya existe le suma la cantidad.
        Retorna 'insertado', 'sumado' o 'error'.
        """
        existe = self.select("SELECT id, cantidad FROM libro WHERE titulo = %s", (titulo,))
        if not existe:
            sql = ("INSERT INTO libro(titulo, id_autor, id_editorial, id_materia, "
                   "cantidad, num_pagina, anio_edicion, descripcion, imagen) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'logo.png')")
            ok = self.save(sql, (titulo, id_autor, id_editorial, id_materia,
                                 cantidad, num_pagina, anio_edicion, descripcion))
            return "insertado" if ok == 1 else "error"
        else:
            nueva_cantidad = existe['cantidad'] + cantidad
            sql = "UPDATE libro SET cantidad = %s WHERE id = %s"
            ok = self.save(sql, (nueva_cantidad, existe['id']))
            return "sumado" if ok == 1 else "error"
