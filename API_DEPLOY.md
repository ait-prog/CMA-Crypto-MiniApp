#Деплой API на публичный сервер

## Вариант 1: Railway (рекомендуется, бесплатно)

### Шаг 1: Регистрация
1. Перейдите на https://railway.app
2. Зарегистрируйтесь через GitHub

### Шаг 2: Создание проекта
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите репозиторий `CMA-Crypto-MiniApp`
4. Выберите папку `api` как root directory

### Шаг 3: Настройка переменных окружения
В Railway Dashboard → Variables добавьте:
```
CRYPTOPANIC_KEY=ecef6293b2242fb90b6e03175ecb5a4a2e3a3b01
LLM4WEB3_URL=
LLM4WEB3_TOKEN=
PORT=8080
```

### Шаг 4: Настройка деплоя
1. Railway автоматически определит Python проект
2. Убедитесь, что запускается: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. После деплоя получите публичный URL (например: `https://crypto-api.railway.app`)

### Шаг 5: Обновление фронтенда
1. В GitHub репозитории → Settings → Secrets → Actions
2. Добавьте secret: `VITE_API` = ваш Railway URL
3. Пересоберите фронтенд

---

## Вариант 2: Render (бесплатно)

### Шаг 1: Регистрация
1. Перейдите на https://render.com
2. Зарегистрируйтесь через GitHub

### Шаг 2: Создание Web Service
1. Нажмите "New +" → "Web Service"
2. Подключите репозиторий `CMA-Crypto-MiniApp`
3. Настройки:
   - **Name**: `crypto-api`
   - **Root Directory**: `api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Шаг 3: Переменные окружения
```
CRYPTOPANIC_KEY=ecef6293b2242fb90b6e03175ecb5a4a2e3a3b01
LLM4WEB3_URL=
LLM4WEB3_TOKEN=
```

### Шаг 4: Деплой
1. Нажмите "Create Web Service"
2. Дождитесь деплоя
3. Получите URL (например: `https://crypto-api.onrender.com`)

---

## Вариант 3: Fly.io (бесплатно)

### Шаг 1: Установка Fly CLI
```bash
# Windows
iwr https://fly.io/install.ps1 -useb | iex
```

### Шаг 2: Регистрация
```bash
fly auth signup
```

### Шаг 3: Создание fly.toml
Создайте файл `api/fly.toml`:
```toml
app = "crypto-api"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Шаг 4: Деплой
```bash
cd api
fly deploy
fly secrets set CRYPTOPANIC_KEY=ecef6293b2242fb90b6e03175ecb5a4a2e3a3b01
```

---

## Обновление фронтенда после деплоя API

1. Получите публичный URL API (например: `https://crypto-api.railway.app`)

2. В GitHub репозитории:
   - Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `VITE_API`
   - Value: ваш API URL (например: `https://crypto-api.railway.app`)

3. Пересоберите фронтенд:
   - GitHub Actions автоматически запустится при следующем push
   - Или вручную: Actions → Deploy to GitHub Pages → Run workflow

---

## Проверка работы API

После деплоя проверьте:
```bash
curl https://your-api-url.railway.app/healthz
curl https://your-api-url.railway.app/coins
curl https://your-api-url.railway.app/news/bitcoin
```

---

## Troubleshooting

### API не отвечает
- Проверьте логи в Dashboard
- Убедитесь, что переменные окружения установлены
- Проверьте, что порт правильный (Railway использует переменную PORT)

### CORS ошибки
- Убедитесь, что в `api/main.py` CORS настроен правильно:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Или конкретные домены
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Новости не загружаются
- Проверьте, что `CRYPTOPANIC_KEY` установлен
- Проверьте логи API на наличие ошибок
- Убедитесь, что не превышен лимит запросов (100 req/mo для Developer плана)

