#  Настройка GitHub репозитория

## Первоначальная настройка

### 1. Инициализация Git репозитория

```bash
# Если репозиторий еще не инициализирован
git init
git branch -M main
```

### 2. Подключение к GitHub

```bash
git remote add origin https://github.com/ait-prog/CMA-Crypto-MiniApp.git
```

Или если репозиторий уже существует:
```bash
git remote set-url origin https://github.com/ait-prog/CMA-Crypto-MiniApp.git
```

### 3. Первый коммит

```bash
git add .
git commit -m "Initial commit: Crypto MiniApp MVP"
git push -u origin main
```

## Настройка GitHub Pages

### Автоматический деплой через GitHub Actions

1. Перейдите в **Settings** → **Pages** вашего репозитория
2. В разделе **Source** выберите:
   - **Source**: `GitHub Actions`
3. Сохраните изменения

После этого при каждом push в `main` будет происходить автоматический деплой.

### Ручная настройка (если нужно)

1. Перейдите в **Settings** → **Pages**
2. В разделе **Source** выберите:
   - **Source**: `Deploy from a branch`
   - **Branch**: `gh-pages` → `/ (root)`
3. Нажмите **Save**

Затем создайте ветку `gh-pages`:
```bash
git checkout -b gh-pages
git push origin gh-pages
```

## Настройка Secrets для API

Если ваш API размещен на отдельном сервере:

1. Перейдите в **Settings** → **Secrets and variables** → **Actions**
2. Нажмите **New repository secret**
3. Создайте secret:
   - **Name**: `VITE_API`
   - **Value**: URL вашего API (например: `https://crypto-api.railway.app`)

## Структура репозитория

```
CMA-Crypto-MiniApp/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Автоматический деплой фронтенда
├── api/                         # FastAPI бэкенд
├── bot/                         # Telegram бот
├── web/                         # React фронтенд
│   ├── .nojekyll               # Для GitHub Pages
│   └── dist/                   # Билд (не коммитить)
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Проверка деплоя

После push кода:

1. Перейдите во вкладку **Actions**
2. Дождитесь завершения workflow "Deploy to GitHub Pages"
3. После успешного деплоя приложение будет доступно:
   **https://ait-prog.github.io/CMA-Crypto-MiniApp/**

## Обновление бота

После деплоя обновите URL в Telegram:

1. Откройте [@BotFather](https://t.me/BotFather)
2. `/myapps` → выберите бота → **Edit** → **Web App URL**
3. Укажите: `https://ait-prog.github.io/CMA-Crypto-MiniApp/`

## Полезные команды

```bash
# Проверить remote
git remote -v

# Обновить код
git pull origin main

# Добавить изменения
git add .
git commit -m "Описание изменений"
git push origin main

# Просмотр логов деплоя
# GitHub → Actions → Выберите последний workflow
```

## Troubleshooting

### GitHub Actions не запускается
- Проверьте, что файл `.github/workflows/deploy.yml` существует
- Убедитесь, что workflow файл имеет правильный синтаксис YAML
- Проверьте вкладку **Actions** на наличие ошибок

### Деплой падает с ошибкой
- Проверьте логи в **Actions** → последний workflow
- Убедитесь, что все зависимости в `package.json` корректны
- Проверьте, что `package-lock.json` закоммичен

### Страница показывает 404
- Убедитесь, что в `vite.config.js` установлен `base: '/CMA-Crypto-MiniApp/'`
- Проверьте наличие файла `.nojekyll` в `web/` директории
- Убедитесь, что билд создает файлы в `web/dist/`

