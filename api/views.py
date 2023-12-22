from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from .weather_service import get_weather
import json


def mainpage(request):
    return HttpResponse("Service if fine, and its works!")


@require_http_methods(["GET"])
def weather(request, city_name):
    cached_data = cache.get(city_name)
    if cached_data is not None:
        return HttpResponse(
            json.dumps(cached_data, ensure_ascii=False), content_type="application/json"
        )
    weather_info = get_weather(city_name)
    cache.set(city_name, weather_info, 1800)
    return HttpResponse(
        json.dumps(weather_info, ensure_ascii=False), content_type="application/json"
    )
