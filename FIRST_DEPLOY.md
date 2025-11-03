#  Первый деплой на GitHub Pages

## Шаг 1: Инициализация Git репозитория

```bash
# Если Git еще не инициализирован
git init
git branch -M main
```

## Шаг 2: Подключение к GitHub репозиторию

```bash
git remote add origin https://github.com/ait-prog/CMA-Crypto-MiniApp.git
```

Если репозиторий уже существует и подключен:
```bash
git remote set-url origin https://github.com/ait-prog/CMA-Crypto-MiniApp.git
```

## Шаг 3: Первый коммит и push

```bash
# Добавляем все файлы
git add .

# Создаем коммит
git commit -m "Initial commit: Crypto MiniApp MVP with GitHub Pages deployment"

# Отправляем в GitHub
git push -u origin main
```

## Шаг 4: Настройка GitHub Pages

1. Перейдите в ваш репозиторий: https://github.com/ait-prog/CMA-Crypto-MiniApp
2. Откройте **Settings** → **Pages**
3. В разделе **Source** выберите:
   - **Source**: `GitHub Actions`
4. Сохраните изменения (нажмите **Save**)

## Шаг 5: Ожидание деплоя

1. Перейдите во вкладку **Actions** в вашем репозитории
2. Дождитесь завершения workflow "Deploy to GitHub Pages"
3. Проверьте, что деплой завершился успешно (зеленая галочка)

## Шаг 6: Проверка работы

После успешного деплоя приложение будет доступно по адресу:
**https://ait-prog.github.io/CMA-Crypto-MiniApp/**

Откройте ссылку в браузере и проверьте, что приложение загружается.

## Шаг 7: Обновление бота

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/myapps`
3. Выберите вашего бота
4. Выберите **Edit** → **Web App URL**
5. Введите: `https://ait-prog.github.io/CMA-Crypto-MiniApp/`
6. Сохраните изменения

## Шаг 8: Обновление .env

Обновите файл `.env` в корне проекта:

```env
BOT_TOKEN=ваш_токен_от_botfather
WEBAPP_URL=https://ait-prog.github.io/CMA-Crypto-MiniApp/
CRYPTOPANIC_KEY=
LLM4WEB3_URL=
LLM4WEB3_TOKEN=
```



Теперь при каждом push в ветку `main` будет происходить автоматический деплой на GitHub Pages.

## Проверка деплоя

### Проверка в браузере
- Откройте: https://ait-prog.github.io/CMA-Crypto-MiniApp/
- Приложение должно загрузиться
- Проверьте консоль браузера на ошибки

### Проверка в Telegram
1. Найдите вашего бота
2. Отправьте `/start`
3. Нажмите "Open App"
4. Приложение должно открыться из GitHub Pages

## Troubleshooting

### GitHub Actions не запускается
- Проверьте, что файл `.github/workflows/deploy.yml` существует
- Убедитесь, что файл закоммичен и запушен в репозиторий
- Проверьте вкладку **Actions** на наличие workflow

### Деплой падает с ошибкой
- Откройте вкладку **Actions** → выберите последний workflow
- Посмотрите логи сборки
- Убедитесь, что все зависимости указаны в `web/package.json`
- Проверьте, что `package-lock.json` закоммичен

### Страница показывает 404
- Убедитесь, что в `web/vite.config.js` установлен `base: '/CMA-Crypto-MiniApp/'`
- Проверьте наличие файла `web/.nojekyll`
- Пересоберите и задеплойте заново

### API запросы не работают
- Убедитесь, что API сервер доступен и имеет правильные CORS настройки
- Проверьте переменную `VITE_API` в GitHub Secrets (если используете)
- Обновите URL в `web/src/api.js` для продакшена

## Дальнейшие действия

После успешного деплоя:
1.  Фронтенд автоматически деплоится при каждом push
2.  API нужно деплоить отдельно (Railway, Render, Fly.io)
3.  Бот должен быть запущен на сервере или через cloud-решение

## Следующие шаги

- [DEPLOY.md](DEPLOY.md) - подробная информация о деплое
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - настройка репозитория
- Настройка продакшен API (Railway/Render/Fly.io)

