import re

def str_clean(cadena: str) -> str:
    """Sanitiza una cadena de entrada. Equivalente a strClean() en PHP."""
    if cadena is None:
        return ""
    string = str(cadena)
    string = re.sub(r'\s+', ' ', string).strip()
    # Eliminar etiquetas script
    for tag in ['<script>', '</script>', '<script type=>', '<script src>']:
        string = re.sub(re.escape(tag), '', string, flags=re.IGNORECASE)
    # Eliminar patrones SQL injection básicos
    patterns = [
        "SELECT * FROM", "DELETE FROM", "INSERT INTO",
        "SELECT COUNT(*) FROM", "DROP TABLE", "OR '1'='1",
        "OR ´1´=´1", "IS NULL", 'LIKE "', "LIKE '", "LIKE ´",
        'OR "a"="a', "OR 'a'='a", "OR ´a´=´a", "--", "^",
        "[", "]", "=="
    ]
    for p in patterns:
        string = re.sub(re.escape(p), '', string, flags=re.IGNORECASE)
    return string
