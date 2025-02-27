Improvised Terminal – Тестовый проект

Описание
Здесь вы сможете запустить мой тестовый проект и ознакомиться с его работой.

Установка и настройка
Склонируйте репозиторий

git clone https://github.com/Yimanbek/Improvised-Terminal.git
cd improvised-terminal


В корне проекта создайте .env файл и пропишите туда:


В корне проекта создайте .env файл и пропишите туда:

SECRET_KEY = "your-secret-key"
DEBUG = True

DATABASE_URL = "postgresql://your_db_user:your_db_password@db:5432/your_db_name"
USER = "your_db_user"
NAME = "your_db_name"
HOST = localhost
PORT = 5432
PASSWORD = "your_db_password"

CELERY_BROKER_URL = "amqp://your_rabbit_user:your_rabbit_password@your_rabbit_host:your_rabbit_port//"
RABBIT_PORT = "your_rabbit_port"
RABBIT_USER = "your_rabbit_user"
RABBIT_PASSWORD = "your_rabbit_password"



после того как .env файл готов

пропишите эти команды в основной директории проекта (там где находятся файлы manage.py, docker-compose.yaml и dockerfile)
Запустите проект через Docker:
  docker-compose up --build -d

После запуска надо создать администратора.
  docker exec -it improvised-terminal python manage.py createsuperuser 
  Введите email и пароль администратора.         



Доступные API
Админка и документация:

http://127.0.0.1:8000/admin/ – Панель администратора
http://127.0.0.1:8000/docs/ – Документация API

Основной функционал:

Админ создаёт администратора
POST /user/admin/create/
Админ добавляет товары
POST /product/create/
Создание заказа (пользователь)
POST /order/order-create/
Добавление товаров в заказ
POST /order/order-item/add-product/<order_id>/
Просмотр заказа
GET /order/order-paid/<order_id>/
Оплата заказа
POST /order/order-paid/<order_id>/paid/ (параметр amount)
Удаление товаров из заказа (только админ)
DELETE /order/order-item/<order_item_id>/
Редактирование количества товара
PUT/PATCH /order/order-item/<order_item_id>/
Редактирование/Удаление товаров (админ)
PUT/PATCH/DELETE /product/<id>/detail/


Важно
Проект не был задеплоен, так как у меня не было средств на сервер (Droplet).
CI/CD не был настроен, так как без деплоя он избыточен.
Тесты автоматически запускаются при старте проекта.
Бонусные/подарочные карты и скидки не реализованы, так как они не были указаны в ТЗ.
