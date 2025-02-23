import requests


# Function to fetch current weather data for a given city
def get_weather_data(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # Using metric units for temperature in Celsius
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the data as a dictionary
    else:
        return {"error": f"Unable to fetch data: {response.status_code}"}




# Function to fetch 5-day weather forecast data for a given city

def get_forecast_data(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Unable to fetch forecast: {response.status_code}"}
