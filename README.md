# Foodgram EN

> Translated version: [Foodgram RU](#foodgram-ru)


![Build](https://github.com/gutsy51/foodgram/actions/workflows/main.yml/badge.svg)

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

## 📃 Description

Web application for publishing and viewing recipes. Site visitors can look for interesting recipes.
Registered users can create and edit recipes, add to favorites and shopping cart.
From the cart you can form a convenient purchase list and download it as `.txt`.

It is an SPA application on React with backend (REST API) on Django+DRF. Proxy provided by Nginx.
Data storage is carried out in PostgreSQL (production) or in SQLite (locally). 
Docker is responsible for the orchestration.

## 🌐 Endpoints

| Path                          | Description       |
|-------------------------------|-------------------|
| https://example.org/          | Main page         |
| https://example.org/admin     | Admin panel       |
| https://example.org/api/docs/ | API specification |

## 📂 Repository structure
```
foodgram/
├── .dockerignore           # Exclusions for Docker.
├── .gitignore              # Exclusions for Git.
├── .github/workflows       # GitHub Actions (CI/CD pipeline).
├── LICENCE                 # Project license.
├── README.md               # You are here!
├── backend/                # Backend.
│   └── foodgram/             # Django project.            
│       ├── foodgram/           # Configuration.
│       ├── api/                # REST API.
│       ├── recipes/            # Models and admin-panel for recipes.
│       ├── users/              # Models and admin-panel for users.
│       └── db_example.json     # Example database dump.
├── data/                   # Example of ingredients.
├── docs/                   # API specification.
├── frontend/               # Frontend React SPA.
├── infra/                  # Project infrastructure.
│   ├── .env.example          # Example environment variables.
│   ├── docker-compose.yml    # Main docker-compose file.
│   ├── nginx/                # Nginx configuration.
│   └── scripts/              # Backend initialization scripts.
└── postman_collection/     # Postman collection for API testing.
```

## 🚀 Start up
### 1. Install Docker
The assembly of the project is carried out using Docker, install it from the official site:
- [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- [Linux](https://docs.docker.com/engine/install/ubuntu/)

If you work on Windows, you can use [WSL](https://docs.docker.com/docker-for-windows/wsl/) 
to work with Docker.

### 2. Clone the repository
```bash
git clone https://github.com/gutsy51/foodgram.git
```

### 3. Prepare the environment variables
Create a file `./infra/.env` and fill it out by the example of `./Infra/.env.example`.

### 4. Launch the project
```bash
cd .../foodgram/infra/         # Go to the `./infra/`.
docker compose up -d --build   # Launch, assembly, do not show logs.
docker compose logs -f         # View the logs in the follow mode.
```

### 5. Migration and collect statics
While in the directory `./foodgram/infra/`, run:
```bash
./scripts/backend_setup.sh
```

### Extra
**All `docker compose` runs should be called from the `./foodgram/infra/`**
#### Create superuser
```bash
docker compose exec backend python ./foodgram/manage.py createsuperuser
```

#### Load example database
```bash
docker compose exec backend python ./foodgram/manage.py loaddata ./foodgram/db_example.json
```

## 🛠️ Testing
Postman is used for testing. Read more: [Postman README](./postman_collection/README.md)


---


# Foodgram RU

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
| https://example.org/admin     | Панель администратора |
| https://example.org/api/docs/ | Документация к API    |

## 📂 Структура репозитория
```
foodgram/
├── .dockerignore           # Исключения для Docker-сборки.
├── .gitignore              # Исключения для Git.
├── .github/workflows       # GitHub Actions (CI/CD pipeline).
├── LICENCE                 # Лицензия проекта.
├── README.md               # Вы сейчас здесь!
├── backend/                # Серверная часть на Django.
│   └── foodgram/             # Django проект.          
│       ├── foodgram/           # Конфигурация проекта.
│       ├── api/                # REST API.
│       ├── recipes/            # Модели и админка рецептов.
│       ├── users/              # Модели и админка пользователей.
│       └── db_example.json     # Пример дампа базы данных.
├── data/                   # Пример ингредиентов.
├── docs/                   # Спецификация API.
├── frontend/               # Клиентская часть на React (SPA).
├── infra/                  # Инфраструктура проекта.
│   ├── .env.example          # Пример переменных окружения.
│   ├── docker-compose.yml    # Главный файл docker-compose.
│   ├── nginx/                # Конфигурация Nginx.
│   └── scripts/              # Скрипты инициализации backend'а.
└── postman_collection/     # Коллекция Postman для тестирования API.
```

## 🚀 Запуск
### 1. Установите Docker
Сборка проекта осуществляется с помощью Docker, установите его с официального сайта:
- [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- [Linux](https://docs.docker.com/engine/install/ubuntu/)

Если вы работаете на Windows, то можно использовать 
[WSL](https://docs.docker.com/docker-for-windows/wsl/) 
для работы с Docker.

### 2. Клонируйте репозиторий
```bash
git clone https://github.com/gutsy51/foodgram.git
```

### 3. Подготовьте переменные окружения
Создайте файл `./infra/.env` и заполните его по примеру `./infra/.env.example`.

### 4. Запустите проект

```bash
cd .../foodgram/infra/         # Переход в директорию `./infra/`.
docker compose up -d --build   # Запуск, сборка, без открытия логов.
docker compose logs -f         # Просмотр логов в режиме следования.
```

### 5. Выполните миграции и соберите статику
Находясь в директории `./foodgram/infra/`
```bash
./scripts/backend_setup.sh
```

### Дополнительно
**Все команды `docker compose` должны вызываться из директории `./foodgram/infra/`**
#### Создайте суперпользователя
```bash
docker compose exec backend python ./foodgram/manage.py createsuperuser
```

#### Заполните базу примером данных
```bash
docker compose exec backend python ./foodgram/manage.py loaddata ./foodgram/db_example.json
```

## 🛠️ Тестирование
Для тестирования используется Postman. Подробнее: [README](./postman_collection/README.md)

---

> Developed by: [gutsy51](https://github.com/gutsy51)