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
git clone https://github.com/Samosta018/fslayers.git
cd fslayers
```

### 2. Настройка виртуального окружения
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Запуск БД
(Требуется добавить в PATH)
```bash
psql -U имя_пользователя -c "CREATE DATABASE fslayers;"
```

или

создать БД через pgAdmin4

### 5. Настройка .env
```bash
copy .env.example .env
```
Отредактируйте .env файл, заполнив свои значения

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Запуск проекта
```bash
python manage.py runserver
```
