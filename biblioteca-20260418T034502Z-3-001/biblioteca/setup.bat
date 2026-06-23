@echo off
REM Script de setup inicial para Biblioteca
REM Ejecutar como: setup.bat

echo.
echo ========================================
echo   SETUP BIBLIOTECA - SCRIPT DE INICIO
echo ========================================
echo.

REM Cambiar al directorio correcto
cd /d "%~dp0"

echo [1/5] Verificando estructura...
if not exist "biblioteca_python" (
    echo ERROR: Directorio biblioteca_python no encontrado
    exit /b 1
)
echo ✓ Estructura correcta

echo.
echo [2/5] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "temp" mkdir temp
echo ✓ Directorios listos

echo.
echo [3/5] Generando claves de seguridad...
python biblioteca_python\admin.py secrets
echo ✓ Claves generadas (copia SECRET_KEY y JWT_SECRET a .env)

echo.
echo [4/5] Ejecutando migraciones...
python biblioteca_python\migrate.py
echo ✓ Migraciones completadas

echo.
echo [5/5] Iniciando aplicación...
python biblioteca_python\app.py

echo.
echo ========================================
echo   Setup completado!
echo   Acceder: http://localhost:5000
echo ========================================
pause
