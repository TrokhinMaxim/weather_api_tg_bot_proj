import unittest
from unittest.mock import patch
from weather_service import get_coordinates, is_valid_city_name, get_weather
from telegram_bot import is_django_server_running


class WeatherServiceTests(unittest.TestCase):
    @patch("geopy.geocoders.Nominatim.geocode")
    def test_get_coordinates_valid_city(self, mock_geocode):
        mock_geocode.return_value.latitude = 50.0
        mock_geocode.return_value.longitude = 30.0
        city_name = "Киев"
        coordinates = get_coordinates(city_name)
        self.assertEqual(coordinates, {"latitude": 50.0, "longitude": 30.0})

    def test_get_coordinates_invalid_city(self):
        city_name = "InvalidCity"
        coordinates = get_coordinates(city_name)
        self.assertEqual(coordinates, {"error": "Указанный город не найден."})

    def test_is_valid_city_name_valid(self):
        city_name = "Санкт-Петербург"
        result = is_valid_city_name(city_name)
        self.assertTrue(result)

    def test_is_valid_city_name_invalid(self):
        city_name = "Invalid City"
        result = is_valid_city_name(city_name)
        self.assertFalse(result)

    def test_get_weather_valid_city(self):
        city_name = "Санкт-Петербург"
        weather_info = get_weather(city_name)
        self.assertNotIn("error", weather_info)

    def test_get_weather_invalid_city(self):
        city_name = "Invalid City"
        weather_info = get_weather(city_name)
        self.assertIn("error", weather_info)
