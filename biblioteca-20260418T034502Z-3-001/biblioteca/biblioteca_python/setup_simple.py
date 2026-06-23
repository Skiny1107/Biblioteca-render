#!/usr/bin/env python3
"""
Script de setup no-interactivo para Biblioteca
Uso: python setup_simple.py
"""

import os
import sys
import secrets
from pathlib import Path

# Agregar ruta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup():
    print("=" * 70)
    print("SETUP SIMPLIFICADO BIBLIOTECA")
    print("=" * 70)
    print()

    # Paso 1: Crear directorios
    print("[1/4] Creando directorios...")
    dirs = ["logs", "uploads", "temp"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"  ✓ {dir_name}/")
    print()

    # Paso 2: Generar claves
    print("[2/4] Generando claves de seguridad...")
    secret_key = secrets.token_urlsafe(32)
    jwt_secret = secrets.token_urlsafe(32)
    print(f"  SECRET_KEY: {secret_key}")
    print(f"  JWT_SECRET: {jwt_secret}")

    # Verificar .env
    env_file = ".env"
    if Path(env_file).exists():
        content = Path(env_file).read_text()
        if "SECRET_KEY=" in content and secret_key not in content:
            print("  ⚠ .env ya existe, actualizar manualmente si es necesario")
    print()

    # Paso 3: Ejecutar migraciones
    print("[3/4] Ejecutando migraciones...")
    try:
        from database import Query
        from logger import setup_logging
        setup_logging()

        db = Query()

        # Migración 1.0: Indexes
        print("  Agregando indexes...")
        index_sqls = [
            "ALTER TABLE usuarios ADD INDEX idx_usuario (usuario)",
            "ALTER TABLE usuarios ADD INDEX idx_estado (estado)",
            "ALTER TABLE autor ADD INDEX idx_autor_nombre (autor)",
            "ALTER TABLE libro ADD INDEX idx_libro_titulo (titulo(191))",
            "ALTER TABLE estudiante ADD INDEX idx_estudiante_codigo (codigo)",
            "ALTER TABLE estudiante ADD INDEX idx_estudiante_estado (estado)",
            "ALTER TABLE prestamo ADD INDEX idx_prestamo_estudiante (id_estudiante)",
            "ALTER TABLE prestamo ADD INDEX idx_prestamo_libro (id_libro)",
            "ALTER TABLE prestamo ADD INDEX idx_prestamo_estado (estado)",
        ]

        for sql in index_sqls:
            try:
                db.save(sql, ())
                print(f"    ✓ Index creado")
            except Exception as e:
                msg = str(e).lower()
                if 'duplicate' in msg or 'exists' in msg:
                    print("    INFO Index ya existe")
                else:
                    print(f"    WARN {str(e)[:50]}")

        db.close()
        print("  ✓ Migraciones completadas")
    except Exception as e:
        print(f"  ⚠ Error en migraciones: {e}")
    print()

    # Paso 4: Crear usuario admin
    print("[4/4] Creando usuario admin...")
    try:
        from database import Query
        from security import SecurityUtils

        username = "admin"
        email = "admin@biblioteca.local"
        password = "Admin123456"

        hash_pass = SecurityUtils.hash_password(password)

        db = Query()

        # Verificar si ya existe
        check_sql = "SELECT id FROM usuarios WHERE usuario = %s"
        result = db.select(check_sql, (username,))

        if result:
            print(f"  ℹ Usuario '{username}' ya existe")
        else:
            insert_sql = "INSERT INTO usuarios(usuario, nombre, clave, estado) VALUES (%s, %s, %s, 1)"
            user_id = db.insert(insert_sql, (username, email, hash_pass))

            if user_id:
                print(f"  ✓ Usuario '{username}' creado")
                print(f"    Usuario: {username}")
                print(f"    Contraseña: {password}")
            else:
                print(f"  ❌ Error al crear usuario")

        db.close()
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        print(f"    (Esto es normal si MySQL aún no está conectado)")

    print()
    print("=" * 70)
    print("✅ SETUP COMPLETADO")
    print("=" * 70)
    print()
    print("PRÓXIMOS PASOS:")
    print("1. Asegúrate que MySQL está corriendo")
    print("2. Ejecuta la aplicación:")
    print("   python biblioteca_python/app.py")
    print("3. Accede a: http://localhost:5000")
    print("4. Credenciales default:")
    print("   Usuario: admin")
    print("   Contraseña: Admin123456")
    print()

if __name__ == "__main__":
    try:
        os.chdir(os.path.join(os.path.dirname(__file__), ".."))
        setup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
