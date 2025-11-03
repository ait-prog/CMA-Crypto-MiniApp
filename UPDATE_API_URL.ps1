# Скрипт для обновления API URL в фронтенде
param(
    [Parameter(Mandatory=$true)]
    [string]$ApiUrl
)

$apiJsPath = "web\src\api.js"

if (Test-Path $apiJsPath) {
    Write-Host "Обновление API URL в web/src/api.js..." -ForegroundColor Cyan
    
    $content = Get-Content $apiJsPath -Raw
    
    # Обновляем API URL
    $newContent = $content -replace 'const API = .+?;', "const API = `"$ApiUrl`";"
    
    Set-Content -Path $apiJsPath -Value $newContent -Encoding UTF8
    
    Write-Host "[OK] API URL обновлен: $ApiUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "Теперь перезапустите фронтенд:" -ForegroundColor Yellow
    Write-Host "  cd web" -ForegroundColor White
    Write-Host "  npm run dev" -ForegroundColor White
} else {
    Write-Host "[ERROR] Файл web/src/api.js не найден!" -ForegroundColor Red
}

