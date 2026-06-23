import sys
import os

# Bootstrapping para permitir ejecucion directa si es necesario
if __name__ == "__main__" or __package__ is None:
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    if parent not in sys.path:
        sys.path.append(parent)

from flask import Blueprint, request, jsonify, session
from database import Query
from models.materia_model import MateriaModel
from logger import get_logger

api_bp = Blueprint('api', __name__, url_prefix='/api')
logger = get_logger('app')

@api_bp.route('/books/', methods=['GET'])
def get_books():
    try:
        q = request.args.get('q', '').strip()
        titulo = request.args.get('titulo', '').strip()
        autor = request.args.get('autor', '').strip()
        categoria = request.args.get('categoria', '').strip()
        editorial = request.args.get('editorial', '').strip()
        anio = request.args.get('anio', '').strip()
        
        db = Query()

        # SQL base con LEFT JOINs — compatible con PostgreSQL
        sql = (
            "SELECT l.id, l.titulo, l.descripcion, l.cantidad, l.num_pagina, "
            "EXTRACT(YEAR FROM l.anio_edicion)::int AS anio, l.imagen, m.materia, "
            "a.autor, e.editorial, l.cantidad AS stock_total, "
            "(l.cantidad - COALESCE((SELECT SUM(p.cantidad) FROM prestamo p "
            "WHERE p.id_libro = l.id AND p.estado = 1), 0)) AS ejemplares_disponibles "
            "FROM libro l "
            "LEFT JOIN materia m ON l.id_materia = m.id "
            "LEFT JOIN autor a ON l.id_autor = a.id "
            "LEFT JOIN editorial e ON l.id_editorial = e.id "
            "WHERE l.estado = 1"
        )

        params = []
        if q or titulo or autor or categoria or editorial or anio:
            if q:
                sql += " AND (l.titulo ILIKE %s OR a.autor ILIKE %s OR e.editorial ILIKE %s OR l.descripcion ILIKE %s OR m.materia ILIKE %s)"
                search_term = f"%{q}%"
                params.extend([search_term, search_term, search_term, search_term, search_term])
            if titulo:
                sql += " AND l.titulo ILIKE %s"
                params.append(f"%{titulo}%")
            if autor:
                sql += " AND a.autor ILIKE %s"
                params.append(f"%{autor}%")
            if categoria:
                sql += " AND m.materia = %s"
                params.append(categoria)
            if editorial:
                sql += " AND e.editorial ILIKE %s"
                params.append(f"%{editorial}%")
            if anio:
                try:
                    sql += " AND EXTRACT(YEAR FROM l.anio_edicion) = %s"
                    params.append(int(anio))
                except ValueError:
                    pass
            sql += " ORDER BY l.titulo LIMIT 100"
        else:
            sql += " ORDER BY l.id DESC LIMIT 200"
        
        libros = db.select_all(sql, tuple(params)) if params else db.select_all(sql)
        db.close()

        return jsonify({
            'success': True,
            'libros': libros or [],
            'count': len(libros) if libros else 0
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_books: {e}")
        return jsonify({
            'success': False,
            'error': 'Error al consultar libros',
            'libros': [],
            'count': 0
        }), 500

@api_bp.route('/books/categorias', methods=['GET'])
def get_categorias():
    try:
        db = Query()
        # Consulta directa para asegurar la conexion con la landing page
        categorias = db.select_all("SELECT materia FROM materia WHERE estado = 1 ORDER BY materia ASC")
        db.close()
        
        return jsonify({
            'success': True,
            'categorias': categorias or []
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_categorias: {e}")
        return jsonify({
            'success': False,
            'error': 'Error al consultar categorías',
            'categorias': []
        }), 500
