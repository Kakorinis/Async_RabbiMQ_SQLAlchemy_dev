### develop - текущая ветка разработки

### Данный проект пример монорепозитория для микросервисов для единого продукта:
- __user_service__: сервис регистрации пользователей.
- __authentication_service__:  сервис хранения учетных данных пользователей.

### Стек технологий:
* использование своего кастомного ядра.
* SQLAlchemy: ОРМ, асинхронка.
* FastAPI
* aio-pika: асинхронный обмен данными между двумя сервисами через рэббита