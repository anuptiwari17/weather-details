import requests

# Function to fetch current weather data for a given city
def get_weather_data(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # Using metric units for temperature in Celsius
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()  # Returns the data as a dictionary
        elif response.status_code == 404:
            return {"error": f"City '{city_name}' not found. Please check the spelling and try again."}
        else:
            return {"error": f"Unable to fetch data: Error {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

# Function to fetch 5-day weather forecast data for a given city
def get_forecast_data(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            # Process the data to filter one forecast per day
            data = response.json()
            
            # Keep only forecasts at 12:00 PM for each day to show daily forecast
            # This is optional - you can remove this filtering if you want 3-hour intervals
            # filtered_list = []
            # dates_added = set()
            # for item in data.get("list", []):
            #     date = item["dt_txt"].split()[0]
            #     if date not in dates_added:
            #         filtered_list.append(item)
            #         dates_added.add(date)
            # data["list"] = filtered_list
            
            return data
        elif response.status_code == 404:
            return {"error": f"City '{city_name}' not found. Please check the spelling and try again."}
        else:
            return {"error": f"Unable to fetch forecast: Error {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}