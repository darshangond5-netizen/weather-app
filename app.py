from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city."
        elif not API_KEY:
            error = "Weather API key is missing."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "humidity": data["main"]["humidity"],
                        "condition": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"],
                        "wind": round(data["wind"]["speed"] * 3.6, 1)
                    }
                elif response.status_code == 404:
                    error = "City not found. Try another city."
                else:
                    error = "Unable to get weather data."

            except requests.RequestException:
                error = "Could not connect to the weather service."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)