# Foodgram

![Build](https://github.com/gutsy51/foodgram/actions/workflows/main.yml/badge.svg)

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

## 📃 Описание

Сайт для публикации и просмотра рецептов. Посетители сайта могут изучить публикации пользователей.
Пользователи же могут рецепты создавать и редактировать, добавлять в избранное и корзину.
Из корзины можно сформировать удобный список покупок и скачать его.

Представляет собой SPA приложение на React, REST API на Django и связывающий их Nginx.
Хранение данных осуществляется в PostgreSQL (продакшн) и в SQLite (локально). 
За оркестровку отвечает Docker.

## 🌐 Адреса

| Адрес                         | Описание              |
|-------------------------------|-----------------------|
| https://example.org/          | Главная страница      |
| https://example.org/admin/    | Панель администратора |
| https://example.org/api/docs/ | Документация к API    |

## 🚀 Запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/gutsy51/foodgram.git
cd foodgram
```

### 2. Подготовьте переменные окружения
Создайте файл `./infra/.env` и заполните его по примеру `./infra/.env.example`.

### 3. Запустите проект
### 3.1. Локальный запуск (`runserver`, только Django)
#### 3.1.1. Установите зависимости
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3.1.2. Настройте БД (в dev-режиме используется SQLite)
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py loaddata ../data/ingredients.json
```
#### 3.1.3. Запустите сервер
```bash
python manage.py runserver
```

### 3.2. Полный запуск (`docker`, весь проект)
**Все команды `docker compose` должны вызываться из директории `./foodgram/infra/`**


#### 3.2.1. Соберите проект и запустите контейнеры
```bash
cd infra
```
```bash
docker compose up -d --build   # Запуск, сборка, без открытия логов.
docker compose logs -f         # Просмотр логов в режиме следования.
```

#### 3.2.2. Выполните миграции и соберите статику
```bash
./scripts/backend_setup.sh
```

#### 3.2.3. Создайте суперпользователя
```bash
docker compose exec backend python ./foodgram/manage.py createsuperuser
```

#### 3.2.4 Импортируйте ингредиенты
```bash
docker compose exec backend python manage.py loaddata ./data/ingredients.json
```


## 🛠️ Тестирование
Для тестирования используется Postman. Подробнее: [README](./postman_collection/README.md)

---

> Автор: Валерий Полуянов, GitHub: [gutsy51](https://github.com/gutsy51), Telegram: [@gutsy51](https://t.me/gutsy51)
