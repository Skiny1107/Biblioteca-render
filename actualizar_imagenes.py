
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import sys
import time
import urllib.request
import urllib.parse
import json
import shutil
import psycopg2
import psycopg2.extras
from datetime import datetime
from biblioteca_python.config import HOST, USER, PASS, DB, DB_PORT

# ─── Configuración de la BD ──────────────────────────────────────────────────
# ─── Rutas de imágenes (relativas al script) ─────────────────────────────────
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
APP_DIR       = os.path.join(SCRIPT_DIR, "biblioteca_python")
IMG_LIBROS    = os.path.join(APP_DIR, "static", "img", "libros")
IMG_AUTORES   = os.path.join(APP_DIR, "static", "img", "autores")

# Imagen por defecto que indica "sin foto todavía"
DEFAULT_IMG   = "logo.png"

# Pausa entre peticiones a APIs externas (segundos) para no saturar
DELAY_SECS    = 0.8

# Timeout para descargar imágenes
TIMEOUT       = 10

# ─── Contadores ──────────────────────────────────────────────────────────────
ok_libros  = 0
ok_autores = 0
fail       = 0
skip       = 0

# ─── Progreso JSON ───────────────────────────────────────────────────────────
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "temp", "progreso_imagenes.json")

def write_progress(estado, total, actual, mensaje):
    try:
        os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
        data = {
            "estado": estado,
            "total": total,
            "actual": actual,
            "mensaje": mensaje,
            "ok_libros": ok_libros,
            "ok_autores": ok_autores
        }
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

# =============================================================================
#  UTILIDADES
# =============================================================================

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "  [OK]", "WARN": "  [!!]", "ERR": "  [XX]", "HEAD": "\n=="}
    print(f"{prefix.get(level,'   ')} [{ts}] {msg}")


def http_get_json(url, params=None):
    """GET JSON con User-Agent amigable. Devuelve dict o None."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "BibliotecaScript/1.0 (biblioteca-local)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return None


def descargar_imagen(url, dest_path):
    """Descarga una imagen desde url y la guarda en dest_path. Retorna True/False."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "BibliotecaScript/1.0 (biblioteca-local)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            content = r.read()
        # Verificar que sea imagen real (al menos 5 KB)
        if len(content) < 5000:
            return False
        with open(dest_path, "wb") as f:
            f.write(content)
        return True
    except Exception:
        return False


def generar_nombre(prefijo, ext="jpg"):
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefijo}_{ts}.{ext}"


# =============================================================================
#  BÚSQUEDA DE PORTADAS - OPEN LIBRARY
# =============================================================================

def buscar_portada_libro(titulo, autor):
    """
    Busca la portada de un libro en Open Library.
    Devuelve (url_imagen, ext) o (None, None).
    """
    # Intentar con título + autor
    data = http_get_json(
        "https://openlibrary.org/search.json",
        {"q": f"{titulo} {autor}", "limit": 5, "fields": "cover_i,title"}
    )
    time.sleep(DELAY_SECS)

    cover_id = None
    if data and data.get("docs"):
        for doc in data["docs"]:
            if doc.get("cover_i"):
                cover_id = doc["cover_i"]
                break

    # Si no encontró, intentar solo con título
    if not cover_id:
        data2 = http_get_json(
            "https://openlibrary.org/search.json",
            {"title": titulo, "limit": 5, "fields": "cover_i,title"}
        )
        time.sleep(DELAY_SECS)
        if data2 and data2.get("docs"):
            for doc in data2["docs"]:
                if doc.get("cover_i"):
                    cover_id = doc["cover_i"]
                    break

    if cover_id:
        # L = large, M = medium
        url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        return url, "jpg"

    return None, None


# =============================================================================
#  BÚSQUEDA DE FOTO DE AUTOR - WIKIPEDIA
# =============================================================================

def buscar_foto_autor(nombre_autor):
    """
    Busca la foto de un autor en Wikipedia (Wikimedia).
    Devuelve (url_imagen, ext) o (None, None).
    """
    # Paso 1: buscar el artículo en Wikipedia
    data = http_get_json(
        "https://en.wikipedia.org/w/api.php",
        {
            "action": "query",
            "list": "search",
            "srsearch": nombre_autor,
            "srlimit": 3,
            "format": "json"
        }
    )
    time.sleep(DELAY_SECS)

    if not data or not data.get("query", {}).get("search"):
        # Intentar en español
        data = http_get_json(
            "https://es.wikipedia.org/w/api.php",
            {
                "action": "query",
                "list": "search",
                "srsearch": nombre_autor,
                "srlimit": 3,
                "format": "json"
            }
        )
        time.sleep(DELAY_SECS)
        wiki_base = "https://es.wikipedia.org"
    else:
        wiki_base = "https://en.wikipedia.org"

    if not data or not data.get("query", {}).get("search"):
        return None, None

    page_title = data["query"]["search"][0]["title"]

    # Paso 2: obtener imagen principal de la página
    data2 = http_get_json(
        f"{wiki_base}/w/api.php",
        {
            "action": "query",
            "titles": page_title,
            "prop": "pageimages",
            "pithumbsize": 400,
            "format": "json"
        }
    )
    time.sleep(DELAY_SECS)

    if not data2:
        return None, None

    pages = data2.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            continue
        thumb = page.get("thumbnail", {})
        if thumb.get("source"):
            url = thumb["source"]
            # Intentar subir resolución
            url = url.replace("/200px-", "/400px-")
            ext = url.rsplit(".", 1)[-1].lower()
            if ext not in ("jpg", "jpeg", "png", "webp"):
                ext = "jpg"
            return url, ext

    return None, None


# =============================================================================
#  CONEXIÓN A LA BASE DE DATOS
# =============================================================================

def conectar_db():
    try:
        url = os.getenv('DATABASE_URL', '')
        if url:
            if url.startswith('postgres://'):
                url = 'postgresql://' + url[len('postgres://'):]
            con = psycopg2.connect(url)
        else:
            con = psycopg2.connect(
                host=HOST, user=USER, password=PASS,
                dbname=DB, port=DB_PORT
            )
        return con
    except Exception as e:
        log(f"No se pudo conectar a la BD: {e}", "ERR")
        sys.exit(1)


# =============================================================================
#  PROCESAR LIBROS
# =============================================================================

def procesar_libros(con):
    global ok_libros, fail, skip
    log("PROCESANDO LIBROS", "HEAD")
    os.makedirs(IMG_LIBROS, exist_ok=True)

    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT l.id, l.titulo, l.imagen, a.autor "
        "FROM libro l "
        "LEFT JOIN autor a ON l.id_autor = a.id "
        "ORDER BY l.id"
    )
    libros = cur.fetchall()
    cur.close()

    total = len(libros)
    log(f"Total de libros en BD: {total}")
    write_progress("procesando_libros", total, 0, "Iniciando escaneo de libros...")

    for i, libro in enumerate(libros, 1):
        id_     = libro["id"]
        titulo  = libro["titulo"] or ""
        autor   = libro["autor"] or ""
        img_act = libro["imagen"] or DEFAULT_IMG

        # Verificar si ya tiene imagen propia
        img_path = os.path.join(IMG_LIBROS, img_act)
        ya_tiene = (
            img_act != DEFAULT_IMG
            and img_act != ""
            and os.path.isfile(img_path)
        )

        if ya_tiene:
            log(f"[{i}/{total}] SKIP  → '{titulo}' (ya tiene imagen)")
            skip += 1
            continue

        log(f"[{i}/{total}] Buscando portada: '{titulo}' / '{autor}'")
        url, ext = buscar_portada_libro(titulo, autor)

        if not url:
            log(f"       No se encontró portada en Open Library", "WARN")
            fail += 1
            continue

        nombre = generar_nombre("libro", ext)
        dest   = os.path.join(IMG_LIBROS, nombre)

        try:
            if descargar_imagen(url, dest):
                # Actualizar BD
                cur2 = con.cursor()
                cur2.execute("UPDATE libro SET imagen=%s WHERE id=%s", (nombre, id_))
                con.commit()
                cur2.close()
                log(f"       ✔ Guardado: {nombre}")
                ok_libros += 1
            else:
                log(f"       No se pudo descargar la imagen", "WARN")
                fail += 1
        except Exception as err:
            log(f"       Error actualizando base de datos para libro {titulo}: {err}", "ERR")
            fail += 1

        write_progress("procesando_libros", total, i, f"Libro {i}/{total}: {titulo}")
        time.sleep(0.2)


# =============================================================================
#  PROCESAR AUTORES
# =============================================================================

def procesar_autores(con):
    global ok_autores, fail, skip
    log("PROCESANDO AUTORES", "HEAD")
    os.makedirs(IMG_AUTORES, exist_ok=True)

    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, autor, imagen FROM autor ORDER BY id")
    autores = cur.fetchall()
    cur.close()

    total = len(autores)
    log(f"Total de autores en BD: {total}")
    write_progress("procesando_autores", total, 0, "Iniciando escaneo de autores...")

    for i, autor in enumerate(autores, 1):
        id_     = autor["id"]
        nombre  = autor["autor"] or ""
        img_act = autor["imagen"] or DEFAULT_IMG

        # Verificar si ya tiene imagen propia
        img_path = os.path.join(IMG_AUTORES, img_act)
        ya_tiene = (
            img_act != DEFAULT_IMG
            and img_act != ""
            and os.path.isfile(img_path)
        )

        if ya_tiene:
            log(f"[{i}/{total}] SKIP  → '{nombre}' (ya tiene imagen)")
            skip += 1
            continue

        log(f"[{i}/{total}] Buscando foto: '{nombre}'")
        url, ext = buscar_foto_autor(nombre)

        if not url:
            log(f"       No se encontró foto en Wikipedia", "WARN")
            fail += 1
            continue

        nombre_archivo = generar_nombre("autor", ext)
        dest = os.path.join(IMG_AUTORES, nombre_archivo)

        try:
            if descargar_imagen(url, dest):
                cur2 = con.cursor()
                cur2.execute("UPDATE autor SET imagen=%s WHERE id=%s", (nombre_archivo, id_))
                con.commit()
                cur2.close()
                log(f"       ✔ Guardado: {nombre_archivo}")
                ok_autores += 1
            else:
                log(f"       No se pudo descargar la imagen", "WARN")
                fail += 1
        except Exception as err:
            log(f"       Error actualizando base de datos para autor {nombre}: {err}", "ERR")
            fail += 1

        write_progress("procesando_autores", total, i, f"Autor {i}/{total}: {nombre}")
        time.sleep(0.2)


# =============================================================================
#  MAIN
# =============================================================================

def main():
    print("=" * 62)
    print("  ACTUALIZADOR AUTOMÁTICO DE IMÁGENES - BIBLIOTECA")
    print("=" * 62)
    print(f"  Carpeta libros : {IMG_LIBROS}")
    print(f"  Carpeta autores: {IMG_AUTORES}")
    print("=" * 62)

    con = conectar_db()
    log("Conexión a BD establecida correctamente")

    procesar_libros(con)
    procesar_autores(con)

    con.close()

    print("\n" + "=" * 62)
    print("  RESUMEN FINAL")
    print("=" * 62)
    print(f"  Portadas de libros actualizadas : {ok_libros}")
    print(f"  Fotos de autores  actualizadas  : {ok_autores}")
    print(f"  Omitidos (ya tenían imagen)     : {skip}")
    print(f"  Fallidos (no encontrados)       : {fail}")
    print("=" * 62)
    print("\n  ¡Listo! Reinicia la aplicación para ver los cambios.")
    
    write_progress("completado", 100, 100, "¡Proceso Completado!")


if __name__ == "__main__":
    main()
