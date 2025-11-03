#  Деплой на GitHub Pages

## Настройка GitHub Pages

### Шаг 1: Настройка репозитория

1. Перейдите в **Settings** → **Pages** вашего репозитория
2. В разделе **Source** выберите:
   - **Source**: `GitHub Actions`
3. Сохраните изменения

### Шаг 2: Настройка Secrets (для продакшен API)

Если у вас есть отдельный API сервер для продакшена:

1. Перейдите в **Settings** → **Secrets and variables** → **Actions**
2. Создайте новый secret:
   - **Name**: `VITE_API`
   - **Value**: URL вашего продакшен API (например: `https://api.yourdomain.com`)

Если не создадите secret, приложение будет использовать дефолтный URL из `web/src/api.js`

### Шаг 3: Push кода в репозиторий

```bash
# Если репозиторий еще не инициализирован
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ait-prog/CMA-Crypto-MiniApp.git
git push -u origin main
```

### Шаг 4: Проверка деплоя

1. Перейдите в **Actions** вкладку репозитория
2. Дождитесь завершения workflow "Deploy to GitHub Pages"
3. После успешного деплоя приложение будет доступно по адресу:
   **https://ait-prog.github.io/CMA-Crypto-MiniApp/**

## Обновление WebApp URL в боте

После деплоя обновите URL в Telegram боте:

1. Найдите [@BotFather](https://t.me/BotFather)
2. Отправьте `/myapps`
3. Выберите вашего бота
4. Выберите **Edit** → **Web App URL**
5. Укажите: `https://ait-prog.github.io/CMA-Crypto-MiniApp/`
6. Обновите `.env` файл:
   ```env
   WEBAPP_URL=https://ait-prog.github.io/CMA-Crypto-MiniApp/
   ```

## Локальная разработка

Для локальной разработки ничего не меняется:

```bash
cd web
npm run dev
```

Приложение запустится на `http://localhost:5173` с правильными путями.

## Продакшен API

GitHub Pages статический хостинг, поэтому API должен быть на отдельном сервере.

### Варианты размещения API:

1. **Railway** (https://railway.app) - бесплатный tier
2. **Render** (https://render.com) - бесплатный tier
3. **Fly.io** (https://fly.io) - бесплатный tier
4. **Ваш собственный VPS**

После деплоя API:
1. Обновите secret `VITE_API` в GitHub
2. Или обновите дефолтное значение в `web/src/api.js`:
   ```javascript
   const API = import.meta.env.VITE_API || "https://your-api-domain.com";
   ```
3. Пересоберите и задеплойте фронтенд

## Автоматический деплой

После настройки GitHub Actions деплой происходит автоматически при каждом push в ветку `main`.

Процесс:
1. Push кода → GitHub Actions запускается
2. Сборка фронтенда → `npm run build`
3. Деплой на GitHub Pages

## Troubleshooting

### Проблема: 404 ошибка на страницах
- Убедитесь, что в `vite.config.js` установлен правильный `base: '/CMA-Crypto-MiniApp/'`
- Проверьте, что файл `.nojekyll` присутствует в `web/` директории

### Проблема: API запросы не работают
- Проверьте CORS настройки на API сервере (должен разрешать запросы с `https://ait-prog.github.io`)
- Обновите `VITE_API` secret в GitHub
- Проверьте, что API доступен по указанному URL

### Проблема: Билд падает
- Проверьте логи в GitHub Actions
- Убедитесь, что все зависимости указаны в `package.json`
- Проверьте, что `package-lock.json` закоммичен

## Структура файлов для GitHub Pages

```
CMA-Crypto-MiniApp/
├── .github/
│   └── workflows/
│       └── deploy.yml        # Автоматический деплой
├── web/
│   ├── .nojekyll              # Отключает Jekyll на GitHub Pages
│   ├── dist/                  # Билд (генерируется автоматически)
│   └── ...
└── ...
```

