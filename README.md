# FSLAYERS

Сайт для фрилансеров


## 🚀 Быстрый старт

### Предварительные требования
- Python 3.10+
- PostgreSQL 15+
- Git
- VS Code (рекомендуется)

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-username/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Настройка виртуального окружения
python -m venv .venv
.venv\Scripts\activate

### 3. Установка зависимостей
pip install -r requirements.txt

### 4. Запуск БД
(Требуется добавить в PATH)
psql -U имя_пользователя -c "CREATE DATABASE fslayers_db;"

или

создать БД через pgAdmin4

### 5. Настройка .env
copy .env.example .env
Отредактируйте .env файл, заполнив свои значения

### 6. Применение миграций
python manage.py migrate

### 7. Запуск проекта
python manage.py runserver