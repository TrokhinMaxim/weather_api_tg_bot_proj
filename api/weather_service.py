import requests
import geopy.exc
from geopy.geocoders import Nominatim
import re

API_KEY = "YOUR_YANDEX_WEATHER_API_KEY"
URL = "https://api.weather.yandex.ru/v2/forecast?"
LANG = "ru_RU"
HEADERS = {"X-Yandex-API-Key": API_KEY}
geolocator = Nominatim(user_agent="get_coords")


def get_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name)
        if not location:
            return {"error": "Указанный город не найден."}
        latitude = location.latitude
        longitude = location.longitude
        return {"latitude": latitude, "longitude": longitude}
    except geopy.exc.GeocoderQueryError as e:
        return {"error": f"Error: {e}"}


def is_valid_city_name(city_name):
    return all(
        word.replace("-", "").isalpha()
        and all(char.isalpha() and char.isalpha() for char in word)
        for word in city_name.split()
    )


def is_valid_city_name(city_name):
    return all(
        (word.replace("-", "").isalpha() and re.match(r"^[А-Яа-яЁё-]+$", word))
        for word in city_name.split()
    )


def get_weather(city_name):
    if not city_name or not is_valid_city_name(city_name):
        return {"error": "Некорректное название города."}

    city_coord = get_coordinates(city_name)
    if "error" in city_coord:
        return city_coord

    LAT = str(city_coord["latitude"])
    LON = str(city_coord["longitude"])

    response = requests.request(
        "GET", f"{URL}&lat={LAT}&lon={LON}&lang={LANG}", headers=HEADERS
    )

    geo_object = response.json().get("geo_object")
    if (
        not geo_object
        or "locality" not in geo_object
        or "name" not in geo_object["locality"]
    ):
        return {"error": "Некорректные данные о городе в ответе от сервиса погоды."}

    city_name = geo_object["locality"]["name"]

    fact = response.json().get("fact")
    if not fact:
        return {"error": "Данные о погоде не найдены в ответе от сервиса погоды."}

    city_temp = fact.get("temp")
    city_pressure_mm = fact.get("pressure_mm")
    city_windspeed = fact.get("wind_speed")

    weather_info = {
        "city_name": city_name,
        "temperature": city_temp,
        "pressure_mm": city_pressure_mm,
        "wind_speed": city_windspeed,
    }

    return weather_info
