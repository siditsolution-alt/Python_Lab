import requests
from requests.exceptions import RequestException, Timeout, HTTPError
from dotenv import load_dotenv
from weather_logger import get_logger
import os

logger = get_logger()

# Load environment variables once at module load time
load_dotenv()

def get_city_weather(city):
    if not city:
        logger.warning("No city provided to get_city_weather")
        return {"temperature": None, "temperature_f": None, "humidity": None, "condition": "Unknown"}

    # Use the city parameter in the query and add a timeout
    url = get_weather_api_url(city)

    try:
        # Make a GET request with a timeout and raise for non-2xx responses
        weather_response = requests.get(url, timeout=10)
        weather_response.raise_for_status()

        # Parse JSON safely
        weather_data = weather_response.json()
        weather_info = handle_weather_api_response(weather_data)

        # Return the weather info directly as a flat dictionary
        return weather_info

    except Timeout:
        logger.exception("Request timed out fetching weather for %s", city)
        return {"temperature": None, "temperature_f": None, "humidity": None, "condition": "Unavailable"}
    except HTTPError:
        logger.exception("HTTP error fetching weather for %s", city)
    except RequestException:
        logger.exception("Network error fetching weather for %s", city)
    except ValueError:
        logger.exception("Invalid JSON response for %s", city)
    except Exception:
        logger.exception("Unexpected error fetching weather for %s", city)

    # If anything failed above, return a safe default matching the original shape
    return {"temperature": None, "temperature_f": None, "humidity": None, "condition": "Unknown"}

def get_weather_api_url(city):
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = os.getenv("WEATHER_API_BASE_URL", "http://api.weatherapi.com/v1")
    
    if not api_key:
        logger.error("WEATHER_API_KEY environment variable is not set or empty")
        raise ValueError("WEATHER_API_KEY environment variable is not set or empty")
        
    url = f"{base_url}/current.json?key={api_key}&q={city}&aqi=no"
    return url

def handle_weather_api_response(weather_data):
    current = weather_data.get('current', {})

    weather_info = {
            "temperature": current.get('temp_c'),
            "temperature_f": current.get('temp_f'),
            "humidity": current.get('humidity'),
            "condition": current.get('condition', {}).get('text', "Unknown"),
        }
    
    return weather_info