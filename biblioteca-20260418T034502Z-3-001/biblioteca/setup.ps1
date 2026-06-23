# Script de Setup para Biblioteca
# Ejecutar como: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SETUP BIBLIOTECA - SCRIPT POWERSHELL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio correcto
Set-Location $PSScriptRoot
Write-Host "Directorio: $(Get-Location)" -ForegroundColor Yellow

# Paso 1: Verificar estructura
Write-Host "[1/5] Verificando estructura..." -ForegroundColor Cyan
if (-not (Test-Path "biblioteca_python")) {
    Write-Host "ERROR: Directorio biblioteca_python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Estructura correcta" -ForegroundColor Green

# Paso 2: Crear directorios
Write-Host "[2/5] Creando directorios..." -ForegroundColor Cyan
$dirs = @("logs", "uploads", "temp")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✓ Directorios listos" -ForegroundColor Green

# Paso 3: Generar claves
Write-Host "[3/5] Verificando claves de seguridad..." -ForegroundColor Cyan
$envFile = ".env"
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    if ($content -match "SECRET_KEY=\S+") {
        Write-Host "✓ Claves ya configuradas" -ForegroundColor Green
    } else {
        Write-Host "⚠ Ejecutando: python biblioteca_python\admin.py secrets" -ForegroundColor Yellow
        & python biblioteca_python/admin.py secrets
    }
} else {
    Write-Host "ERROR: Archivo .env no encontrado" -ForegroundColor Red
    exit 1
}

# Paso 4: Migraciones
Write-Host "[4/5] Ejecutando migraciones..." -ForegroundColor Cyan
Write-Host "Ejecutando: python biblioteca_python\migrate.py" -ForegroundColor Yellow
& python biblioteca_python/migrate.py
Write-Host "✓ Migraciones completadas" -ForegroundColor Green

# Paso 5: Crear usuario admin
Write-Host "[5/5] Crear usuario admin..." -ForegroundColor Cyan
Write-Host "Ejecutando: python biblioteca_python\admin.py admin" -ForegroundColor Yellow
& python biblioteca_python/admin.py admin

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Setup completado exitosamente!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximo paso: Iniciar la aplicación" -ForegroundColor Yellow
Write-Host "Comando: python biblioteca_python\app.py" -ForegroundColor Yellow
Write-Host "URL: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
