import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os


API_KEY = '1e0b3978016240d3882115645252407' #API Key
BASE_URL = 'http://api.weatherapi.com/v1/current.json'
OUTPUT_IMAGE_FILENAME = 'weather_dashboard.png'

# Fetch Weather Data
def fetch_weather_data(city_name):
    """
    Fetches current weather data for a given city from WeatherAPI.com.

    Args:
        city_name (str): The name of the city.

    Returns:
        dict: A dictionary containing the relevant weather data if successful, otherwise None.
    """
    if not city_name:
        print("Error: City name cannot be empty.")
        return None

    try:
        url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses
        data = response.json()

        # Extracting relevant data
        weather_info = {
            'location_name': data['location']['name'],
            'country': data['location']['country'],
            'temp_c': data['current']['temp_c'],
            'temp_f': data['current']['temp_f'],
            'feelslike_c': data['current']['feelslike_c'],
            'feelslike_f': data['current']['feelslike_f'],
            'condition_text': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'wind_kph': data['current']['wind_kph'],
            'wind_dir': data['current']['wind_dir'],
            'pressure_mb': data['current']['pressure_mb'],
            'vis_km': data['current']['vis_km'],
            'uv_index': data['current']['uv']
        }
        return weather_info

    except requests.exceptions.HTTPError as http_err:
        error_data = response.json()
        error_msg = error_data.get('error', {}).get('message', 'An unknown HTTP error occurred.')
        print(f"HTTP Error for '{city_name}': {error_msg}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Network or connection error: {req_err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Create Visualizations and Dashboard
def create_weather_dashboard(weather_data, output_filename=OUTPUT_IMAGE_FILENAME):
    """
    Generates a dashboard with current weather visualizations and saves it as an image.

    Args:
        weather_data (dict): Dictionary containing current weather information.
        output_filename (str): The name of the file to save the dashboard.
    """
    if not weather_data:
        print("No weather data provided to create dashboard.")
        return

    sns.set_style("whitegrid")
    sns.set_palette("deep") #different palette for distinct metrics

    fig, axes = plt.subplots(2, 2, figsize=(18, 14)) 
    fig.suptitle(f"Current Weather Dashboard for {weather_data['location_name']}, {weather_data['country']}",
                 fontsize=28, fontweight='bold', y=1.02)

    #Temperature Overview
    temps = pd.DataFrame({
        'Metric': ['Temperature (°C)', 'Feels Like (°C)', 'Temperature (°F)', 'Feels Like (°F)'],
        'Value': [weather_data['temp_c'], weather_data['feelslike_c'],
                  weather_data['temp_f'], weather_data['feelslike_f']]
    })
    sns.barplot(x='Metric', y='Value', data=temps, ax=axes[0, 0], palette='coolwarm')
    axes[0, 0].set_title('Temperature Overview', fontsize=18)
    axes[0, 0].set_ylabel('Value', fontsize=14)
    axes[0, 0].set_xlabel('')
    axes[0, 0].tick_params(axis='x', labelsize=12)
    axes[0, 0].bar_label(axes[0,0].containers[0], fmt='%.1f') # Display values on bars

    # Humidity and Wind Speed
    # Using a bar plot for these two key metrics
    metrics = pd.DataFrame({
        'Metric': ['Humidity (%)', 'Wind Speed (kph)'],
        'Value': [weather_data['humidity'], weather_data['wind_kph']]
    })
    sns.barplot(x='Metric', y='Value', data=metrics, ax=axes[0, 1], palette='crest')
    axes[0, 1].set_title('Humidity & Wind Speed', fontsize=18)
    axes[0, 1].set_ylabel('Value', fontsize=14)
    axes[0, 1].set_xlabel('')
    axes[0, 1].tick_params(axis='x', labelsize=12)
    axes[0, 1].bar_label(axes[0,1].containers[0], fmt='%.1f')

    # Atmospheric Pressure & Visibility
    pressure_vis = pd.DataFrame({
        'Metric': ['Pressure (mb)', 'Visibility (km)'],
        'Value': [weather_data['pressure_mb'], weather_data['vis_km']]
    })
    sns.barplot(x='Metric', y='Value', data=pressure_vis, ax=axes[1, 0], palette='magma')
    axes[1, 0].set_title('Pressure & Visibility', fontsize=18)
    axes[1, 0].set_ylabel('Value', fontsize=14)
    axes[1, 0].set_xlabel('')
    axes[1, 0].tick_params(axis='x', labelsize=12)
    axes[1, 0].bar_label(axes[1,0].containers[0], fmt='%.1f')

    #Weather Condition and Wind Direction
    #text information
    axes[1, 1].axis('off') 
    axes[1, 1].text(0.5, 0.8, f"Condition: {weather_data['condition_text']}",
                    fontsize=20, ha='center', va='center', wrap=True)
    axes[1, 1].text(0.5, 0.5, f"Wind Direction: {weather_data['wind_dir']}",
                    fontsize=20, ha='center', va='center', wrap=True)
    axes[1, 1].text(0.5, 0.2, f"UV Index: {weather_data['uv_index']}",
                    fontsize=20, ha='center', va='center', wrap=True)


    plt.tight_layout(rect=[0, 0.03, 1, 0.98])

    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved as '{output_filename}'")

   
# --- s Execution ---
if __name__ == "__main__":
    # Get city name from user input when running the script
    city = input("Enter city name for weather dashboard: ")
    if city:
        weather_data = fetch_weather_data(city)
        if weather_data:
            create_weather_dashboard(weather_data)
        else:
            print(f"Failed to fetch weather data for {city}. Dashboard not created.")
    else:
        print("No city name entered. Exiting.")