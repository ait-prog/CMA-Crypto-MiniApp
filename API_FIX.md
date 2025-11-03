# 🔧 Исправление проблем с API

## Проблемы

1. **NetworkError** - API недоступен из Telegram
2. **Нет данных** графиков и новостей

## Причины

### 1. NetworkError
- API работает на `localhost:8081`
- Telegram не может обращаться к localhost
- Нужен публичный URL

### 2. Нет новостей
- CryptoPanic API Developer план имеет ограничения:
  - Задержка 24 часа
  - Лимит 100 запросов/месяц
  - Возможно, новости еще не доступны

## Решения

### Вариант 1: Использовать ngrok (быстрое тестирование)

1. **Запустите ngrok:**
   ```powershell
   .\START_NGROK.ps1
   ```
   Или вручную:
   ```bash
   ngrok http 8081
   ```

2. **Скопируйте HTTPS URL** (например: `https://abc123.ngrok.io`)

3. **Обновите API URL:**
   ```powershell
   .\UPDATE_API_URL.ps1 -ApiUrl "https://abc123.ngrok.io"
   ```

4. **Пересоберите фронтенд:**
   ```bash
   cd web
   npm run build
   ```

5. **Обновите GitHub Secrets:**
   - Settings → Secrets → Actions
   - Добавьте: `VITE_API` = ваш ngrok URL
   - Пересоберите фронтенд через GitHub Actions

### Вариант 2: Деплой на Railway (рекомендуется)

1. **Следуйте инструкции:** `RAILWAY_SETUP.md`

2. **После деплоя:**
   - Скопируйте публичный URL (например: `https://crypto-api.railway.app`)
   - Обновите GitHub Secrets: `VITE_API` = ваш Railway URL
   - Пересоберите фронтенд

### Проверка новостей

Developer план CryptoPanic имеет задержку 24 часа. Если новости не появляются:

1. Проверьте логи API:
   ```bash
   # В логах Railway или локально
   # Должно быть: [News] API Key length: 40
   # Должно быть: [News] Request params: currencies=BTC, filter=hot
   ```

2. Проверьте лимит запросов:
   - Developer план: 100 запросов/месяц
   - Проверьте, не превышен ли лимит

3. Проверьте формат ответа:
   ```bash
   curl "https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_KEY&currencies=BTC&filter=hot&public=true"
   ```

## Проверка работы API

После деплоя проверьте:

```bash
# Health check
curl https://your-api-url.railway.app/healthz

# Список монет
curl https://your-api-url.railway.app/coins

# Цена Bitcoin
curl https://your-api-url.railway.app/price/bitcoin

# График Bitcoin
curl https://your-api-url.railway.app/ohlc/bitcoin?days=30

# Новости Bitcoin
curl https://your-api-url.railway.app/news/bitcoin

# Анализ Bitcoin
curl -X POST https://your-api-url.railway.app/analysis/bitcoin
```

## После исправления

1. Обновите `VITE_API` в GitHub Secrets
2. Пересоберите фронтенд (автоматически через GitHub Actions)
3. Проверьте приложение в Telegram

