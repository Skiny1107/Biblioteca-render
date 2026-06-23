@echo off
REM Script de Inicio - Biblioteca
REM Configuración Clásica Estándar

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          BIBLIOTECA - SETUP AUTOMÁTICO CLÁSICO             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Cambiar directorio
cd /d "%~dp0"

if not exist "biblioteca_python" (
    echo ERROR: Directorio biblioteca_python no encontrado
    pause
    exit /b 1
)

echo.
echo [1/5] Verifying directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "temp" mkdir temp
echo ✓ Directorios listos

echo.
echo [2/5] Checking MySQL connection...
set MYSQL_CMD=mysql
where %MYSQL_CMD% >nul 2>&1
if errorlevel 1 (
    if exist "C:\xampp\mysql\bin\mysql.exe" (
        set MYSQL_CMD="C:\xampp\mysql\bin\mysql.exe"
    )
)

%MYSQL_CMD% -u root -e "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo ✗ MySQL no está corriendo en puerto 3306 o no se encuentra el ejecutable.
    echo.
    echo SOLUCIÓN:
    echo 1. Abre XAMPP Control Panel
    echo 2. Click Start en MySQL
    echo 3. Espera a que diga "Running"
    echo 4. Corre este script de nuevo
    echo.
    pause
    exit /b 1
)
echo ✓ MySQL conectado correctamente (127.0.0.1:3306)

echo.
echo [3/5] Checking database...
%MYSQL_CMD% -u root -e "USE biblioteca" >nul 2>&1
if errorlevel 1 (
    echo ✗ Base de datos no existe
    echo.
    echo Importando schema...
    %MYSQL_CMD% -u root < biblioteca.sql
    if errorlevel 1 (
        echo ERROR: No se pudo importar la BD
        pause
        exit /b 1
    )
    echo ✓ Base de datos importada
) else (
    echo ✓ Base de datos existe
)

echo.
echo [4/5] Running setup...
python biblioteca_python\setup_simple.py
if errorlevel 1 (
    echo ERROR: Setup falló
    pause
    exit /b 1
)
echo ✓ Setup completado

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║            ✅ SETUP COMPLETADO EXITOSAMENTE               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo SIGUIENTE PASO:
echo.
echo   python biblioteca_python\app.py
echo.
echo ACCEDER:
echo.
echo   http://127.0.0.1:5000
echo   Usuario: admin
echo   Contraseña: Admin123456
echo.
pause
