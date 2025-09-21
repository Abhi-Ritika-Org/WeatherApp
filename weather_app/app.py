from datetime import datetime
from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("OWM_API_KEY")


# Jinja2 filter to format datetime
@app.template_filter("datetime")
def format_datetime(value):
    """Convert string or UNIX timestamp to human-readable date"""
    try:
        # If value is a string from forecast
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%b %d %H:%M")
    except:
        # If value is a UNIX timestamp
        return datetime.fromtimestamp(value).strftime("%b %d %H:%M")


# Weather by city
@app.route("/", methods=["GET", "POST"])
def index():
    city = request.form.get("city") or request.args.get("city")
    weather = {}
    forecast = []
    search_type = "manual"  # Default to manual search
    error_message = None

    if city and API_KEY:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") == 200:
            weather = {
                "city": res["name"],
                "country": res["sys"]["country"],
                "temperature": res["main"]["temp"],
                "humidity": res["main"]["humidity"],
                "wind": res["wind"]["speed"],
                "condition": res["weather"][0]["description"],
            }

            # Forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            res_forecast = requests.get(forecast_url).json()
            forecast = [
                {
                    "dt": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "condition": item["weather"][0]["description"]
                }
                for item in res_forecast.get("list", [])[:5]
            ]
        else:
            error_message = f"City '{city}' not found. Please check the spelling and try again."
    elif not API_KEY:
        error_message = "API key not found. Please set OWM_API_KEY in .env file."

    return render_template("index.html", weather=weather, forecast=forecast, search_type=search_type, error_message=error_message)


# Weather by coordinates (latitude & longitude)
@app.route("/coords")
def coords_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    weather = {}
    forecast = []
    search_type = "location"
    error_message = None

    if API_KEY and lat and lon:
        # Current weather
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") == 200:
            weather = {
                "city": res["name"],
                "country": res["sys"]["country"],
                "temperature": res["main"]["temp"],
                "humidity": res["main"]["humidity"],
                "wind": res["wind"]["speed"],
                "condition": res["weather"][0]["description"],
            }

            # Forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            res_forecast = requests.get(forecast_url).json()
            forecast = [
                {
                    "dt": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "condition": item["weather"][0]["description"]
                }
                for item in res_forecast.get("list", [])[:5]
            ]
        else:
            error_message = "Unable to get weather data for your location."
    elif not API_KEY:
        error_message = "API key not found. Please set OWM_API_KEY in .env file."
    else:
        error_message = "Location coordinates not provided."

    return render_template("index.html", weather=weather, forecast=forecast, search_type=search_type, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
