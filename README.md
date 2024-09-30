# Stockroom API

## Описание

Stockroom API - это RESTful API для управления заказами и продуктами. API предоставляет возможности для создания, чтения, обновления и удаления заказов и продуктов, а также для управления статусами заказов.

## Структура проекта
```
stockroomAPI
├───.env-non-dev
├───.idea
├───alembic.ini
├───docker
├───docker-compose.yml
├───Dockerfile
├───pyproject.toml
├───src
│   ├───api
│   │   │───order.py
│   │   │───product.py
│   │   └───routers.py
│   ├───db
│   │   │───config.py
│   │   └───database.py
│   ├───main.py
│   ├───migrations
│   │   ├───versions_
│   │   ├───env.py
│   │   ├───README
│   │   └───script.py.mako
│   ├───models
│   │   │───order.py
│   │   └────product.py
│   ├───repositories
│   │   │───order.py
│   │   └────product.py
│   └───schemas
│       │───order.py
│       │───orderItem.py
│       └────product.py
├───tests
│   │───conftest.py
│   │───order_tests.py
│   └────product_tests.py
│
└───README.md
```
## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL репозитория>
cd stockroomAPI
```

### 2. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл .env в корне проекта и скопируйте в него содержимое .env-non-dev:

```bash
DB_HOST = host.docker.internal(для файла .env-non-dev)
DB_PORT = yourport
DB_USER = youruser
DB_PASS = yourpass
DB_NAME = yourdbname

POSTGRES_DB=yourdbname
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpass

TEST_DB_HOST = yourtestdbhost
TEST_DB_PORT = yourtestdbport
TEST_DB_USER = yourtestdbuser
TEST_DB_PASS = yourtestdbpass
TEST_DB_NAME = yourtestdbname
```
Заполните файлы .env и .env-non-dev своими данными для подключения к бд и тестовым бд.

### 4. Запуск приложения
#### С использованием Docker

Постройте и запустите контейнеры Docker:

```bash
docker compose build
docker compose up
```

#### Без использования Docker

1. Запустите PostgreSQL сервер и создайте базу данных.
2. Выполните миграции Alembic.

```bash   
alembic revision --autogenerate -m "Initial migration" 
alembic upgrade head
```

3. Запустите приложение:
```bash
python src\main.py 
```

#### Используйте SwagerUI для документирования и проверки функцианальности
После запуска перейдите по ссылке `http://<your_host>:8000/docs#/`.

### 5. Запуск тестов

Перед запуском тестов, замените функцию 'get_url' на 'get_test_url' в файле src/migrations/env.py

```bash
url = get_test_url() # строка 39
connectable = create_async_engine(get_test_url(), poolclass=pool.NullPool) # строка 55
```

Запустите тесты:
```bash
pytest
```

## API Роутеры

### Продукты
- POST /api/products/: Создание нового продукта.
- GET /api/products/: Получение списка всех продуктов.
- GET /api/products/{product_id}: Получение информации о продукте по ID.
- PUT /api/products/{product_id}: Обновление информации о продукте.
- DELETE /api/products/{product_id}: Удаление продукта.

### Заказы
- POST /api/orders/: Создание нового заказа.
- GET /api/orders/: Получение списка всех заказов.
- GET /api/orders/{order_id}: Получение информации о заказе по ID.
- PUT /api/orders/{order_id}/status: Обновление статуса заказа.
- DELETE /api/orders/{order_id}: Удаление заказа.