import os
import requests
from dotenv import load_dotenv

# Read the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")


class Weather:
    """Stores weather data for one city."""

    def __init__(self, city, country, temperature, feels_like, humidity, description):
        self.city = city
        self.country = country
        self.temperature = temperature
        self.feels_like = feels_like
        self.humidity = humidity
        self.description = description

    def summary(self):
        return (
            "=" * 30 + "\n"
            f"  Weather in {self.city}, {self.country}\n"
            + "=" * 30 + "\n"
            f"  Condition   : {self.description}\n"
            f"  Temperature : {self.temperature:.1f}°C\n"
            f"  Feels like  : {self.feels_like:.1f}°C\n"
            f"  Humidity    : {self.humidity}%\n"
            + "=" * 30
        )


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(url, params=params)

    if response.status_code == 401:
        print("API key is invalid or not active yet. Wait a bit and try again.")
        return None
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json().get('message')}")
        return None

    data = response.json()
    return Weather(
        city=data["name"],
        country=data["sys"]["country"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"].title(),
    )


if __name__ == "__main__":
    if not API_KEY:
        print("API_KEY not found. Check your .env file.")
    else:
        weather = get_weather("Cairo")
        if weather:
            print(weather.summary())