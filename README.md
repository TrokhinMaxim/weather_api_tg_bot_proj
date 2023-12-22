# Проект "weather_api_tg_bot_proj"

Тестовое задание для компании ТЛ Групп.

## О проекте

Проект включает в себя две части:
- **Django API:** API для получения информации о погоде через HTTP-запросы.
- **Telegram бот:** Бот, предоставляющий прогноз погоды через Telegram.

## Структура проекта

- `api_tg_weather`: Django-приложение с API для получения погоды.
- `telegram_bot`: Telegram-бот на основе Aiogram.
- `weather_service`: Модуль для взаимодействия с API погоды.
- Unit-тесты в файле tests.py

## Запуск проекта

1. **Django API:**
   ```bash
   Установите зависимости pip install -r requirements.txt
   Перейдите в директорию проекта cd api_tg_weather
   Запустите сервер python manage.py runserver

   
   ## Важно! Телеграм бот будет работать только в случае, если запущен локальный сервер
