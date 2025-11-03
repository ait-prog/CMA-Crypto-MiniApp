#  Пошаговая инструкция по запуску MVP

## Шаг 1: Создание Telegram бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Укажите имя бота (например: "Crypto Analyzer Bot")
   - Укажите username бота (например: "crypto_analyzer_bot")
4. Сохраните полученный токен в безопасном месте (например: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 2: Настройка WebApp в боте

1. После создания бота, отправьте BotFather команду `/newapp`
2. Выберите созданного бота
3. Укажите название мини-приложения (например: "Crypto MiniApp")
4. Загрузите изображение (512x512px) или пропустите этот шаг
5. Укажите короткое описание
6. **Важно**: Укажите URL вашего веб-приложения:
   - Для разработки: `http://localhost:5173` (будет работать только через ngrok/tunneling)
   - Для продакшена: ваш домен (например: `https://yourdomain.com`)

## Шаг 3: Создание файла .env

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=ваш_токен_от_botfather
WEBAPP_URL=http://localhost:5173
CRYPTOPANIC_KEY=
LLM4WEB3_URL=
LLM4WEB3_TOKEN=
```

**Примечание**: 
- `CRYPTOPANIC_KEY` - опционально, можно получить на https://cryptopanic.com/developers/api/
- `LLM4WEB3_URL` и `LLM4WEB3_TOKEN` - для интеграции с вашей LLM моделью (опционально)

## Шаг 4: Установка зависимостей

### Вариант A: Запуск через Docker (рекомендуется)

```bash
# Убедитесь, что Docker и Docker Compose установлены
docker-compose up --build
```

### Вариант B: Запуск локально

#### Бэкенд (API):
```bash
cd api
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

#### Фронтенд (WebApp):
```bash
cd web
npm install
npm run dev
```

#### Бот:
```bash
cd bot
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python bot.py
```

## Шаг 5: Настройка tunneling для локальной разработки

Так как Telegram требует HTTPS для WebApp, для локальной разработки используйте туннелирование:

### Использование ngrok:

1. Установите ngrok: https://ngrok.com/download
2. Запустите ngrok:
   ```bash
   ngrok http 5173
   ```
3. Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)
4. Обновите `.env`:
   ```env
   WEBAPP_URL=https://abc123.ngrok.io
   ```
5. Обновите WebApp URL в BotFather командой `/myapps` → выберите бота → Edit → Web App URL

**Для продакшена**: После деплоя на GitHub Pages используйте:
   ```env
   WEBAPP_URL=https://ait-prog.github.io/CMA-Crypto-MiniApp/
   ```
   Подробности о деплое: см. [DEPLOY.md](DEPLOY.md)

### Альтернатива: Cloudflare Tunnel или localtunnel

## Шаг 6: Тестирование

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Нажмите кнопку "Open App"
4. Попробуйте:
   - Поиск криптовалют (например: "bitcoin", "btc", "solana")
   - Переключение между вкладками
   - Просмотр графиков, новостей и анализа рисков

## Шаг 7: Интеграция с LLM4Web3

Если у вас есть LLM4Web3 модель, настроьте её:

1. Убедитесь, что ваша LLM модель доступна по HTTP
2. Модель должна принимать POST запросы:
   ```json
   {
     "coin": "bitcoin",
     "metrics": {
       "rsi": 65.5,
       "ma20": 45000,
       "ma50": 42000,
       "vol30": 0.35,
       "dd30": -0.15
     },
     "news": [...]
   }
   ```
3. Модель должна возвращать:
   ```json
   {
     "summary": "Краткий анализ криптовалюты...",
     "risk_level": "умеренный"
   }
   ```
4. Обновите `.env`:
   ```env
   LLM4WEB3_URL=http://localhost:8001
   LLM4WEB3_TOKEN=your_token_here
   ```

## Проверка работы API

После запуска бэкенда проверьте доступность:

- http://localhost:8080/healthz - должен вернуть `{"ok": true}`
- http://localhost:8080/coins - список монет
- http://localhost:8080/price/bitcoin - цена Bitcoin

## Troubleshooting

### Проблема: Бот не отвечает
- Проверьте правильность `BOT_TOKEN` в `.env`
- Убедитесь, что бот запущен (`python bot.py`)

### Проблема: WebApp не открывается
- Проверьте, что фронтенд запущен на порту 5173
- Убедитесь, что `WEBAPP_URL` в `.env` правильный
- Проверьте URL в BotFather (`/myapps`)

### Проблема: API не отвечает
- Проверьте, что бэкенд запущен на порту 8080
- Проверьте переменную `VITE_API` в `web/.env` (должна быть `http://localhost:8080`)

### Проблема: Новости не загружаются
- Это нормально, если не указан `CRYPTOPANIC_KEY`
- Можно использовать бесплатный API или оставить пустым (будет пустой список)

### Проблема: График не отображается
- Проверьте консоль браузера на ошибки
- Убедитесь, что данные приходят с API (`/ohlc/bitcoin`)

## Дальнейшие шаги

1. Настройте продакшен домен
2. Добавьте SSL сертификат
3. Настройте мониторинг и логирование
4. Добавьте больше индикаторов и функций

