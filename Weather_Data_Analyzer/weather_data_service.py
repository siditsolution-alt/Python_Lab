import pandas as pd
from datetime import datetime
from weather_logger import get_logger
from weather_numpy_analyzer import analyze_weather_data
from weather_panda_data_handler import convert_to_dataframe, inspect_dataframe, save_to_csv
from weather_api_service import get_city_weather
from weather_matplotlib_graph_generator import generate_graphs

logger = get_logger()

def fetch_weather_data(cities):
    """
    Fetch weather data for a list of cities.
    
    Args:
        cities (list): List of city names to fetch weather for
        
    Returns:
        list: List of dictionaries containing weather data
    """
    weather_records = []
    
    for city in cities:
        logger.info(f"Fetching weather data for {city}...")
        weather_info = get_city_weather(city)
        
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'city': city,
            'temperature_c': weather_info.get('temperature'),
            'temperature_f': weather_info.get('temperature_f'),
            'humidity': weather_info.get('humidity'),
            'condition': weather_info.get('condition')
        }
        
        weather_records.append(record)
        logger.info(f"Retrieved weather data for {city}")
    
    return weather_records

def get_weather_data_for_cities(cities, output_file="weather_data.csv"):
    """
    Main function to fetch weather data, convert to DataFrame, inspect, and save.
    
    Args:
        cities (list): List of city names
        output_file (str): Name of the output CSV file
        
    Returns:
        pd.DataFrame: The processed DataFrame
    """
    # Fetch data
    weather_records = fetch_weather_data(cities)
    
    # Convert to DataFrame
    df = convert_to_dataframe(weather_records)
    
    # Inspect DataFrame
    inspect_dataframe(df)

    # Analyze weather data and get statistics
    stats = analyze_weather_data(weather_records, cities)
    
    # Create dashboard with visualizations
    generate_graphs(weather_records, cities, stats)
    
    # Append timestamp to filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = output_file.rsplit('.', 1)
    output_file = f"{name}_{timestamp}.{ext}"
    
    # Save to CSV
    save_to_csv(df, output_file)
    
    return df
