from flask import Flask, render_template, request
import os
from weather_data import get_weather_data, get_forecast_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# API key for OpenWeatherMap
API_KEY = os.getenv("WEATHER_API_KEY", "277b75709af8b2527971d2fc655710cb")

# Function to generate plots
def create_forecast_plots(data):
    df = pd.DataFrame(data)
    df["dt_txt"] = pd.to_datetime(df["dt_txt"])



    # Temperature Heatmap
    # temperature_data = df.pivot(index="dt_txt", columns="temperature", values="humidity")  # Adjust according to your data
    # plt.figure(figsize=(10, 6))
    # sns.heatmap(temperature_data, cmap="coolwarm", annot=True, fmt="f", linewidths=0.5)
    # plt.title("Temperature Heatmap")
    # plt.xlabel("Temperature (°C)")
    # plt.ylabel("Date and Time")
    # plt.tight_layout()
    # plt.savefig("static/temperature_heatmap.png")
    # plt.close()


    # Temperature Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="temperature", data=df, marker="o", label="Temperature (°C)")
    plt.title("Temperature Forecast")
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/temperature_forecast.png")
    plt.close()

    # Humidity Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="humidity", data=df, marker="o", color="blue", label="Humidity (%)")
    plt.title("Humidity Forecast")
    plt.xlabel("Date and Time")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/humidity_forecast.png")
    plt.close()

    # Pressure Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="pressure", data=df, marker="o", color="green", label="Pressure (hPa)")
    plt.title("Pressure Forecast")
    plt.xlabel("Date and Time")
    plt.ylabel("Pressure (hPa)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/pressure_forecast.png")
    plt.close()

    # Wind Speed Plot
   
    plt.figure(figsize=(10, 6))
    sns.barplot(x="dt_txt", y="wind_speed", data=df, color="purple")
    plt.title("Wind Speed Forecast")
    plt.xlabel("Date and Time")
    plt.ylabel("Wind Speed (m/s)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("static/wind_speed_bar.png")
    plt.close()


# Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    forecast_data = []
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # Fetch weather and forecast data
            weather_response = get_weather_data(city, API_KEY)
            forecast_response = get_forecast_data(city, API_KEY)

            # Handle errors from API responses
            if "error" in weather_response:
                error = weather_response["error"]
            elif "error" in forecast_response:
                error = forecast_response["error"]
            else:
                weather = weather_response
                for entry in forecast_response.get("list", []):
                    forecast_data.append({
                        "dt_txt": entry["dt_txt"],
                        "temperature": entry["main"]["temp"],
                        "humidity": entry["main"]["humidity"],
                        "pressure": entry["main"]["pressure"],
                        "wind_speed": entry["wind"]["speed"],
                        "description": entry["weather"][0]["description"],
                    })

                # Generate plots if forecast data exists
                if forecast_data:
                    create_forecast_plots(forecast_data)
        else:
            error = "Please enter a city name."

    return render_template(
        "index.html",
        weather=weather,
        forecast_data=forecast_data,
        error=error,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=10000)









