import sys
import mysql.connector
from werkzeug.security import generate_password_hash

try:
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='biblioteca', port=3306)
    cursor = conn.cursor()
    
    # Generate fresh hash
    new_hash = generate_password_hash('admin', method='pbkdf2:sha256')
    print("New hash generated:", new_hash)
    
    cursor.execute('UPDATE usuarios SET clave = %s WHERE usuario = %s', (new_hash, 'admin'))
    conn.commit()
    print("Updated `admin` in database successfully.")
    
    cursor.execute('SELECT clave FROM usuarios WHERE usuario="admin"')
    row = cursor.fetchone()
    print("Hash in DB:", row[0])
    
    cursor.close()
    conn.close()
except Exception as e:
    print("ERROR:", e)
