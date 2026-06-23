#!/usr/bin/env python3
# type: ignore
import mysql.connector  # type: ignore
import sys

try:
    # Conectar a MySQL
    conn = mysql.connector.connect(
        user='root',
        host='127.0.0.1',
        port=3306
    )
    cursor = conn.cursor()

    # Crear BD si no existe
    cursor.execute('CREATE DATABASE IF NOT EXISTS biblioteca')
    print('✓ Base de datos biblioteca lista')

    # Leer y ejecutar SQL
    with open('biblioteca.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Usar la BD
    cursor.execute('USE biblioteca')

    # Ejecutar SQL
    for statement in sql_content.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                if "already exists" in str(e):
                    pass
                else:
                    print(f'Advertencia: {e}')

    conn.commit()
    print('✓ Schema importado exitosamente')

    # Crear usuario admin
    cursor.execute("INSERT IGNORE INTO usuarios (usuario, nombre, clave, estado) VALUES (%s, %s, %s, %s)",
                   ('admin', 'Administrador',
                    'pbkdf2:sha256:600000$aaa$bbb', 1))
    conn.commit()
    print('✓ Usuario admin creado')

    cursor.close()
    conn.close()
    print('\n✅ TODO LISTO PARA EJECUTAR LA APLICACIÓN')

except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
