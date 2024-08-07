# Api_user_reviews
## Описание:
Проект Api_user_reviews собирает отзывы пользователей на различные произведения.

## Технологии:
- Python 3.9
- Django 3.2
- djangorestframework
- JWT

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/KonstantinSKS/api_user_reviews.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```

После запуска сервера документация к API будет доступна по ссылке:
http://127.0.0.1:8000/redoc/

## Примеры запросов к API:

**GET- запросы:**

эндпоинт /api/v1/titles/ - Получить список всех произведений.

эндпоинт /api/v1/titles/{titles_id}/ - Получение произведения по id.

эндпоинт /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву.

**POST- запросы**
- эндпоинт /api/v1/posts/ - Добавление произведения. Права доступа: Администратор. Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего). При добавлении нового произведения требуется указать уже существующие категорию и жанр.

в body:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

- эндпоинт /api/v1/auth/signup/ - Регистрация нового пользователя. Получить код подтверждения на переданный email. Права доступа: Доступно без токена.

в body:
```
{
  "email": "user@example.com",
  "username": "string"
}
```

Подробную документация к API проекта Yatube и примеры смотри на /redoc/


Авторы: Даниил, Тахен, Константин
