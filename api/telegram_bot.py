import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram import executor
import requests
from weather_service import get_weather

API_TOKEN = "YOUR TELEGRAM BOT API KEY"
DJANGO_SERVER_URL = "http://127.0.0.1:8000/"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_weather = KeyboardButton("Узнать погоду")
keyboard.add(button_weather)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот, который поможет тебе узнать погоду. Нажми кнопку 'Узнать погоду'.",
        reply_markup=keyboard,
    )


@dp.message_handler(lambda message: message.text == "Узнать погоду")
async def get_weather_info(message: types.Message):
    await message.answer("Введите название города:")


@dp.message_handler(
    lambda message: message.text.lower() not in ["узнать погоду", "/start"]
)
async def process_city(message: types.Message):
    city_name = message.text
    weather_info = get_weather(city_name)

    if "error" in weather_info:
        await message.answer(f"Ошибка: {weather_info['error']}")
    else:
        response_text = (
            f"🌇 Погода в городе {weather_info['city_name']}:\n "
            f"🌡 Температура: {weather_info['temperature']}°C\n "
            f"🤿 Давление: {weather_info['pressure_mm']} мм рт. ст.\n "
            f"💨 Скорость ветра: {weather_info['wind_speed']} м/c"
        )
        await message.answer(response_text, parse_mode=ParseMode.MARKDOWN)


def is_django_server_running():
    try:
        response = requests.get(DJANGO_SERVER_URL)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


if is_django_server_running():
    logging.info("Django server is running. Starting the bot.")
    executor.start_polling(dp, skip_updates=True)
else:
    logging.error("Django server is not running. Start the Django server first.")
