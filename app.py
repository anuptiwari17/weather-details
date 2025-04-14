from flask import Flask, render_template, request
import os
from weather_data import get_weather_data, get_forecast_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

app = Flask(__name__)

# API key for OpenWeatherMap
API_KEY = os.getenv("WEATHER_API_KEY", "277b75709af8b2527971d2fc655710cb")

# Template filters for date formatting
@app.template_filter('date_format')
def date_format_filter(timestamp):
    date_obj = datetime.fromtimestamp(timestamp)
    return date_obj.strftime("%A, %b %d, %Y %H:%M")

@app.template_filter('format_date')
def format_date_filter(dt_text):
    date_obj = datetime.strptime(dt_text, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%b %d")

@app.template_filter('format_time')
def format_time_filter(dt_text):
    date_obj = datetime.strptime(dt_text, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%H:%M")

@app.template_filter('visibility_format')
def visibility_format_filter(visibility):
    # Convert visibility from meters to kilometers
    return round(visibility / 1000, 1)

# Function to generate plots
def create_forecast_plots(data):
    df = pd.DataFrame(data)
    df["dt_txt"] = pd.to_datetime(df["dt_txt"])

    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)

    # Set Seaborn style for better looking plots
    sns.set_style("whitegrid")
    
    # Temperature Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="temperature", data=df, marker="o", color="#4361ee", linewidth=3)
    plt.title("Temperature Forecast", fontsize=16, fontweight='bold')
    plt.xlabel("Date and Time", fontsize=12)
    plt.ylabel("Temperature (°C)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("static/temperature_forecast.png", dpi=100, bbox_inches='tight')
    plt.close()

    # Humidity Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="humidity", data=df, marker="o", color="#4895ef", linewidth=3)
    plt.title("Humidity Forecast", fontsize=16, fontweight='bold')
    plt.xlabel("Date and Time", fontsize=12)
    plt.ylabel("Humidity (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("static/humidity_forecast.png", dpi=100, bbox_inches='tight')
    plt.close()

    # Pressure Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="dt_txt", y="pressure", data=df, marker="o", color="#4cc9f0", linewidth=3)
    plt.title("Pressure Forecast", fontsize=16, fontweight='bold')
    plt.xlabel("Date and Time", fontsize=12)
    plt.ylabel("Pressure (hPa)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("static/pressure_forecast.png", dpi=100, bbox_inches='tight')
    plt.close()

    # Wind Speed Plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="dt_txt", y="wind_speed", data=df, color="#3f37c9")
    plt.title("Wind Speed Forecast", fontsize=16, fontweight='bold')
    plt.xlabel("Date and Time", fontsize=12)
    plt.ylabel("Wind Speed (m/s)", fontsize=12)
    plt.xticks(rotation=90)
    
    # Add value labels on top of bars
    for i, p in enumerate(ax.patches):
        ax.annotate(f'{p.get_height():.1f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', 
                    fontsize=9, color='black',
                    xytext=(0, 5), 
                    textcoords='offset points')
    
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("static/wind_speed_bar.png", dpi=100, bbox_inches='tight')
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
                        "icon": entry["weather"][0]["icon"],  # Add weather icon code
                        "feels_like": entry["main"]["feels_like"]  # Add feels like temperature
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=10000)