# Скрипт для запуска ngrok туннеля для API
Write-Host "Запуск ngrok туннеля для API (порт 8081)..." -ForegroundColor Cyan
Write-Host ""
Write-Host "После запуска скопируйте HTTPS URL (например: https://abc123.ngrok.io)" -ForegroundColor Yellow
Write-Host "Обновите web/src/api.js с этим URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "Нажмите Ctrl+C для остановки" -ForegroundColor Gray
Write-Host ""

# Проверка наличия ngrok
if (Get-Command ngrok -ErrorAction SilentlyContinue) {
    ngrok http 8081
} elseif (Test-Path "C:\ngrok\ngrok.exe") {
    & "C:\ngrok\ngrok.exe" http 8081
} else {
    Write-Host "[ERROR] ngrok не найден!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Скачайте ngrok: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "Или используйте деплой на Railway (см. QUICK_DEPLOY.md)" -ForegroundColor Cyan
}

