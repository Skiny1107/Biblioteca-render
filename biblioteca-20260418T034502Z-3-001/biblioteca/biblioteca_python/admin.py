#!/usr/bin/env python3
import os
import sys
import secrets
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_secrets():
    """Generar claves secretas seguras"""
    print("=" * 60)
    print("GENERADOR DE CLAVES SECRETAS")
    print("=" * 60)
    print()

    secret_key = secrets.token_urlsafe(32)
    jwt_secret = secrets.token_urlsafe(32)

    print("Copiar estas claves a tu archivo .env:")
    print()
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET={jwt_secret}")
    print()
    print("⚠️  IMPORTANTE: No compartas estas claves!")
    print()

def create_admin_user():
    """Crear usuario admin"""
    from database import Query
    from security import SecurityUtils

    print("=" * 60)
    print("CREAR USUARIO ADMIN")
    print("=" * 60)
    print()

    try:
        username = input("Usuario: ").strip()
        email = input("Email (opcional): ").strip()
        password = input("Contraseña: ").strip()

        if len(username) < 3:
            print("❌ Usuario debe tener mínimo 3 caracteres")
            return

        if len(password) < 8:
            print("❌ Contraseña debe tener mínimo 8 caracteres")
            return

        hash_pass = SecurityUtils.hash_password(password)

        db = Query()
        sql = "INSERT INTO usuarios(usuario, nombre, clave, estado) VALUES (%s, %s, %s, 1)"
        result = db.insert(sql, (username, email or username, hash_pass))

        if result:
            print(f"✅ Usuario {username} creado exitosamente (ID: {result})")
        else:
            print("❌ Error al crear usuario")

        db.close()
    except Exception as e:
        print(f"❌ Error: {e}")

def reset_password():
    """Resetear contraseña de usuario"""
    from database import Query
    from security import SecurityUtils

    print("=" * 60)
    print("RESETEAR CONTRASEÑA")
    print("=" * 60)
    print()

    try:
        user_id = input("ID del usuario: ").strip()
        new_password = input("Nueva contraseña: ").strip()

        if len(new_password) < 8:
            print("❌ Contraseña debe tener mínimo 8 caracteres")
            return

        hash_pass = SecurityUtils.hash_password(new_password)

        db = Query()
        sql = "UPDATE usuarios SET clave = %s WHERE id = %s"
        result = db.save(sql, (hash_pass, user_id))

        if result:
            print("✅ Contraseña actualizada exitosamente")
        else:
            print("❌ Usuario no encontrado")

        db.close()
    except Exception as e:
        print(f"❌ Error: {e}")

def show_database_info():
    """Mostrar información de la base de datos"""
    from database import Query

    print("=" * 60)
    print("INFORMACIÓN DE BASE DE DATOS")
    print("=" * 60)
    print()

    try:
        db = Query()

        # Usuarios
        users = db.select_all("SELECT COUNT(*) as count FROM usuarios")
        print(f"Usuarios: {users[0]['count'] if users else 0}")

        # Libros
        books = db.select_all("SELECT COUNT(*) as count FROM libro")
        print(f"Libros: {books[0]['count'] if books else 0}")

        # Estudiantes
        students = db.select_all("SELECT COUNT(*) as count FROM estudiante")
        print(f"Estudiantes: {students[0]['count'] if students else 0}")

        # Préstamos
        loans = db.select_all("SELECT COUNT(*) as count FROM prestamo")
        print(f"Préstamos: {loans[0]['count'] if loans else 0}")

        db.close()
        print()
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Herramientas de administración de Biblioteca'
    )
    parser.add_argument(
        'command',
        choices=['secrets', 'admin', 'reset-password', 'info'],
        help='Comando a ejecutar'
    )

    args = parser.parse_args()

    if args.command == 'secrets':
        generate_secrets()
    elif args.command == 'admin':
        create_admin_user()
    elif args.command == 'reset-password':
        reset_password()
    elif args.command == 'info':
        show_database_info()

if __name__ == '__main__':
    main()
