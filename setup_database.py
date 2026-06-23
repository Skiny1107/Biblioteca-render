#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT DE CARGA DE BASE DE DATOS
Carga la base de datos completa en MySQL
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
import argparse
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def load_sql_file(filepath):
    """Cargar archivo SQL"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"{Colors.RED}❌ Error al leer archivo SQL: {e}{Colors.RESET}")
        return None

def execute_sql_script(connection, sql_script):
    """Ejecutar script SQL"""
    try:
        cursor = connection.cursor()

        # Dividir por punto y coma para ejecutar múltiples queries
        statements = sql_script.split(';')

        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.upper().startswith('--'):
                try:
                    cursor.execute(statement)
                    connection.commit()
                except mysql.connector.Error as e:
                    # Ignorar algunos errores no críticos
                    if 'already exists' not in str(e) and 'Unknown procedure' not in str(e):
                        print(f"{Colors.YELLOW}⚠️  Aviso: {e}{Colors.RESET}")

        cursor.close()
        return True
    except Exception as e:
        print(f"{Colors.RED}❌ Error ejecutando SQL: {e}{Colors.RESET}")
        return False

def connect_mysql(host, user, password):
    """Conectar a MySQL sin especificar BD"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            autocommit=False
        )
        return connection
    except Error as e:
        print(f"{Colors.RED}❌ Error de conexión: {e}{Colors.RESET}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Cargar base de datos Biblioteca')
    parser.add_argument('--host', default='localhost', help='Host MySQL (default: localhost)')
    parser.add_argument('--user', default='root', help='Usuario MySQL (default: root)')
    parser.add_argument('--password', default='', help='Contraseña MySQL (default: vacía)')
    parser.add_argument('--file', default='biblioteca_completa.sql', help='Archivo SQL a cargar')

    args = parser.parse_args()

    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}📚 CARGA DE BASE DE DATOS BIBLIOTECA v2.1.0{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    # Verificar archivo SQL
    sql_file = Path(args.file)
    if not sql_file.exists():
        print(f"{Colors.RED}❌ Archivo no encontrado: {args.file}{Colors.RESET}")
        return False

    print(f"{Colors.YELLOW}📁 Archivo SQL: {sql_file.name}{Colors.RESET}")
    print(f"{Colors.YELLOW}🔌 Host: {args.host}{Colors.RESET}")
    print(f"{Colors.YELLOW}👤 Usuario: {args.user}{Colors.RESET}\n")

    # Conectar a MySQL
    print(f"{Colors.BLUE}Conectando a MySQL...{Colors.RESET}")
    connection = connect_mysql(args.host, args.user, args.password)

    if not connection:
        return False

    print(f"{Colors.GREEN}✅ Conectado a MySQL{Colors.RESET}\n")

    # Cargar archivo SQL
    print(f"{Colors.BLUE}Cargando script SQL...{Colors.RESET}")
    sql_script = load_sql_file(args.file)

    if not sql_script:
        return False

    print(f"{Colors.GREEN}✅ Script cargado ({len(sql_script)} bytes){Colors.RESET}\n")

    # Ejecutar script
    print(f"{Colors.BLUE}Ejecutando script SQL...{Colors.RESET}")
    if execute_sql_script(connection, sql_script):
        print(f"{Colors.GREEN}✅ Base de datos cargada exitosamente{Colors.RESET}\n")
    else:
        print(f"{Colors.RED}❌ Error al cargar base de datos{Colors.RESET}\n")
        connection.close()
        return False

    # Verificar BD
    print(f"{Colors.BLUE}Verificando base de datos...{Colors.RESET}")
    try:
        cursor = connection.cursor()

        # Conectar a la BD creada
        cursor.execute("USE biblioteca_db")

        # Contar tablas
        cursor.execute("""
            SELECT COUNT(*) as tablas
            FROM information_schema.tables
            WHERE table_schema = 'biblioteca_db'
        """)
        result = cursor.fetchone()
        num_tablas = result[0] if result else 0

        print(f"{Colors.GREEN}✅ Tablas creadas: {num_tablas}{Colors.RESET}")

        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM libros")
        libros = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        estudiantes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM prestamos")
        prestamos = cursor.fetchone()[0]

        print(f"{Colors.GREEN}✅ Registros:{Colors.RESET}")
        print(f"  - Usuarios: {usuarios}")
        print(f"  - Libros: {libros}")
        print(f"  - Estudiantes: {estudiantes}")
        print(f"  - Préstamos: {prestamos}\n")

        cursor.close()
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Error verificando BD: {e}{Colors.RESET}\n")

    # Cierre
    connection.close()

    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}🎉 BASE DE DATOS LISTA PARA USAR{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    print(f"{Colors.YELLOW}Credenciales de prueba:{Colors.RESET}")
    print(f"  👤 Usuario: admin / bibliotecario / usuario1")
    print(f"  🔐 Contraseña: password\n")

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
