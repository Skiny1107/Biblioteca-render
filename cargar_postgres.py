#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper script for database initialization.
Eliminates code duplication by dynamically importing and executing biblioteca_postgres.sql.
"""

import os
import sys
import importlib.util

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(script_dir, "biblioteca_postgres.sql")
    
    if not os.path.exists(target_path):
        print(f"Error: No se encontró el archivo {target_path}")
        return False
        
    try:
        # Cargamos dinámicamente el archivo biblioteca_postgres.sql como módulo de Python
        spec = importlib.util.spec_from_file_location("biblioteca_postgres", target_path)
        if spec is None or spec.loader is None:
            print("Error: No se pudo crear la especificación del módulo.")
            return False
            
        module = importlib.util.module_from_spec(spec)
        sys.modules["biblioteca_postgres"] = module
        spec.loader.exec_module(module)
        
        # Ejecutamos la función main del script importado
        return module.main()
    except Exception as e:
        print(f"Error cargando o ejecutando biblioteca_postgres.sql: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
