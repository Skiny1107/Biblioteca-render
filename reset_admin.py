#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reset password admin → Admin123!"""
import sys, os
sys.path.insert(0, 'biblioteca_python')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
import psycopg2

nueva_clave = 'Admin123!'
hash_clave = generate_password_hash(nueva_clave, method='pbkdf2:sha256')

conn = psycopg2.connect(host='127.0.0.1', port=5432, dbname='biblioteca',
                        user='postgres', password='K.evin2007')
cur = conn.cursor()
cur.execute("UPDATE usuarios SET clave = %s WHERE usuario = 'admin'", (hash_clave,))
cur.execute("UPDATE usuarios SET clave = %s WHERE usuario = 'angel'", (hash_clave,))
conn.commit()
cur.execute("SELECT id, usuario, rol FROM usuarios WHERE usuario IN ('admin','angel')")
rows = cur.fetchall()
for r in rows:
    print(f"  ID={r[0]} usuario={r[1]} rol={r[2]} -> clave actualizada a: {nueva_clave}")
cur.close()
conn.close()
print("\nListo! Ahora puedes entrar con:")
print("  Usuario: admin")
print("  Clave:   Admin123!")
