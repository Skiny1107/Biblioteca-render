import sys
import os
import subprocess

def main():
    print("\n--- INICIALIZADOR DE BASE DE DATOS RENDER ---")
    print("Ve a Render > Tu base de datos > Copia la 'External Database URL'")
    db_url = input("\nPega la URL aquí: ").strip()
    
    if not db_url:
        print("URL vacía. Cancelando.")
        return
        
    if "postgresql" not in db_url and "postgres" not in db_url:
        print("La URL no parece válida. Debe empezar por postgresql:// o postgres://")
        return
        
    try:
        sql_file = "biblioteca_postgres.sql"
        if not os.path.exists(sql_file):
            print(f"Error: No se encontró el archivo {sql_file}")
            return
            
        print(f"Ejecutando el script de inicialización {sql_file}...")
        
        # Seteamos DATABASE_URL en las variables de entorno para que el script secundario la use
        env = os.environ.copy()
        env["DATABASE_URL"] = db_url
        
        # Ejecutamos biblioteca_postgres.sql como un proceso hijo en Python
        result = subprocess.run([sys.executable, sql_file], env=env, check=True)
        
        if result.returncode == 0:
            print("\n✅ ¡ÉXITO TOTAL! Las tablas han sido creadas en Render.")
            print("✅ Ya puedes ir a tu página web e iniciar sesión con:")
            print("   Usuario: admin")
            print("   Contraseña: admin123 (o la contraseña definida en el script)")
        else:
            print(f"\n❌ El script finalizó con código de error {result.returncode}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al ejecutar el script de inicialización: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
