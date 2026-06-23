# Script de Inicio - Biblioteca (PowerShell)
# Configuración Clásica Estándar

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          BIBLIOTECA - SETUP AUTOMÁTICO CLÁSICO             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Ir al directorio correcto
Set-Location $PSScriptRoot

# Verificar estructura
Write-Host "[1/5] Verificando estructura..." -ForegroundColor Yellow
if (-not (Test-Path "biblioteca_python")) {
    Write-Host "✗ ERROR: Directorio biblioteca_python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Estructura correcta" -ForegroundColor Green

# Crear directorios
Write-Host "[2/5] Creando directorios..." -ForegroundColor Yellow
@("logs", "uploads", "temp") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}
Write-Host "✓ Directorios listos" -ForegroundColor Green

# Verificar MySQL
Write-Host "[3/5] Verificando conexión a MySQL..." -ForegroundColor Yellow
$mysqlCmd = "mysql"
if (-not (Get-Command "mysql" -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\xampp\mysql\bin\mysql.exe") {
        $mysqlCmd = "C:\xampp\mysql\bin\mysql.exe"
    }
}

$mysqlTest = & $mysqlCmd -u root -e "SELECT 1" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ MySQL no está corriendo en puerto 3306 o no se encontró el ejecutable." -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCIÓN:" -ForegroundColor Yellow
    Write-Host "1. Abre XAMPP Control Panel" -ForegroundColor White
    Write-Host "2. Click Start en MySQL" -ForegroundColor White
    Write-Host "3. Espera a que diga 'Running'" -ForegroundColor White
    Write-Host "4. Corre este script de nuevo" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "✓ MySQL conectado correctamente (127.0.0.1:3306)" -ForegroundColor Green

# Verificar BD
Write-Host "[4/5] Verificando base de datos..." -ForegroundColor Yellow
$bdTest = & $mysqlCmd -u root -e "USE biblioteca" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Base de datos no existe" -ForegroundColor Red
    Write-Host "Importando schema..." -ForegroundColor Yellow
    Get-Content "biblioteca.sql" | & $mysqlCmd -u root
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ ERROR: No se pudo importar la BD" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Write-Host "✓ Base de datos importada" -ForegroundColor Green
} else {
    Write-Host "✓ Base de datos existe" -ForegroundColor Green
}

# Setup
Write-Host "[5/5] Ejecutando setup..." -ForegroundColor Yellow
& python biblioteca_python/setup_simple.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Setup falló" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "✓ Setup completado" -ForegroundColor Green

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ SETUP COMPLETADO EXITOSAMENTE               ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "SIGUIENTE PASO:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  python biblioteca_python\app.py" -ForegroundColor White
Write-Host ""
Write-Host "ACCEDER:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  http://127.0.0.1:5000" -ForegroundColor White
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: Admin123456" -ForegroundColor White
Write-Host ""
Read-Host "Presiona Enter para finalizar"
