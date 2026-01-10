# Django + Stripe

Тестовое Django приложение для взаимодействия со Stripe

## Требования

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## Запуск приложения

1. Установить `Требуемые` пакеты.

2. Клонировать репозиторий:

   ```bash
   git clone https://github.com/chiefheston/django-stripe-api-test.git
   cd django-stripe-api-test
   ```

3. Задать переменные окружения

   ```bash
   cp .env.example .env
   ```

   Небоходимо указать `DJANGO_SECRET_KEY` и `STRIPE_API_KEY`

4. Запустить приложение

   ```bash
   make app
   ```

5. Применить миграции

   ```bash
   make migrate
   ```

6. Создать суперпользователя
   ```bash
   make superuser
   ```

Приложение доступно по адресу: http://localhost:8000/

## Ресурсы
- GET `/item/{item_id}` — Получить форму оплаты товара по его id
- GET `/buy/{item_id}` — Получить `client_secret` для `PaymentElement` для оплаты товара
- GET `/order/{order_id}` — Получить форму оплаты заказа по его id
- GET `/order/{order_id}/buy` — Получить `client_secret` для `PaymentElement` для оплаты заказа

### Команды

- `make app` - Поднять приложение
- `make app-shell` - Запуск оболочки контейнера
- `make app-logs` - Следить за логами приложения
- `make app-down` - Остановить приложение
