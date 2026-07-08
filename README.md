# FastAPI Booking API
Проект, выполненный в рамках курса по Backend-разработке. Представляет собой веб-приложение для бронирования отелей и поддерживает такие функции как: написание отзывов и формирование рейтинга на их основе, бронирование номеров и проверка их доступности, добавление отелей и номеров, а также поиск по указанным параметрам и его сортировку.

## Установка
С помощью команды ниже сохраните проект на свой локальный компьютер для дальнейшего запуска:

`git clone https://github.com/two4faced/booking-api.git`

### Запуск через Docker

Перед установкой создайте в корне файл .env и опираясь на .env.example заполните его.

Далее создайте сеть следующей командой:

`docker network create booking-network`

После успешного создания сети установите и запустите образ PostgreSQL, заполнив поля POSTGRES_USER и POSTGRES_PASSWORD в соответствии с вашим .env файлом:

`docker run --name booking_db -p 6432:5432 -e POSTGRES_USER= -e POSTGRES_PASSWORD= -e POSTGRES_DB=booking --network=booking-network -d postgres:18`

Далее требуется установить и запустить образ Redis:

`docker run --name booking_cache -p 7379:6379 --network=booking-network -d redis:7.4`

После успешной установки PostgreSQL и Redis соберите образ проекта:

`docker build -t booking_image .`

А следом запустите его командой:

`docker run --name booking_backend -p 7777:8000 --network=booking-network booking_image`

После успешной установки и запуска по адресу http://127.0.0.1:7777/docs будет доступна автоматическая документация FastAPI, где вы сможете протестировать работу API.