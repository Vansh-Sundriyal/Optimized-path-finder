import requests


class WeatherService:
    """
    Fetches live weather data and converts it into
    routing-relevant flags:
    - rain
    - fog
    - high wind
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, lat: float, lon: float) -> dict:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        weather = {
            "rain": False,
            "fog": False,
            "high_wind": False
        }

        # Rain detection
        if "rain" in data:
            weather["rain"] = True

        # Fog / mist / haze detection
        for w in data.get("weather", []):
            if w.get("main", "").lower() in ["fog", "mist", "haze"]:
                weather["fog"] = True

        # High wind detection (important for bikes & walking)
        wind_speed = data.get("wind", {}).get("speed", 0.0)
        if wind_speed >= 8.0:  # m/s threshold
            weather["high_wind"] = True

        return weather
