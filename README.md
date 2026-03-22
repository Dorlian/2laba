# Playlist Hub

Веб-приложение на Django для создания плейлистов из демо-каталога треков. Каталог и строки интерфейса заданы в коде (списки и словари). Созданные плейлисты хранятся в сессии браузера.

Пользовательские настройки **тема** (светлая / тёмная) и **язык интерфейса** (русский / English), а также список **последних посещённых страниц**, сохраняются в **cookies**.

## Требования

- Python 3.11+ (рекомендуется актуальная стабильная версия)
- pip

## Установка и запуск

Клонируйте репозиторий и перейдите в каталог проекта.

### 1. Виртуальное окружение

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Зависимости

```bash
pip install -r requirements.txt
```

### 3. Миграции и суперпользователь (опционально)

```bash
python manage.py migrate
```

При необходимости создайте учётную запись администратора:

```bash
python manage.py createsuperuser
```

### 4. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 5. Тесты

```bash
python manage.py test
```

## Структура

- `config/` — настройки проекта Django
- `playlists/` — приложение: представления, формы, данные, middleware для cookie «последние страницы»
- `templates/` — шаблоны
- `static/` — CSS и изображения

## Публикация на GitHub

1. Создайте пустой репозиторий на GitHub.
2. В каталоге проекта выполните (подставьте свой URL):

```bash
git remote add origin https://github.com/<username>/<repo>.git
git branch -M main
git push -u origin main
```

Репозиторий не должен содержать папку `venv/` — она указана в `.gitignore`.
