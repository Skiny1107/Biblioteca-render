$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "Cerrando procesos viejos en el puerto 8777..." -ForegroundColor Yellow
$listeners = Get-NetTCPConnection -LocalPort 8777 -State Listen -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique

foreach ($procId in $listeners) {
    try {
        Stop-Process -Id $procId -Force -ErrorAction Stop
        Write-Host "Proceso cerrado: $procId" -ForegroundColor DarkYellow
    } catch {
        Write-Host "No se pudo cerrar el proceso $procId" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Iniciando Biblioteca en http://127.0.0.1:8777" -ForegroundColor Green
Write-Host "Deja esta ventana abierta mientras usas la app." -ForegroundColor Cyan
Write-Host ""

py temp\run8777.py
