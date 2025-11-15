from weather_logger import setup_logging, get_logger
from weather_data_service import get_weather_data_for_cities

# Initialize logging
logger = setup_logging()

if __name__ == "__main__":
    ## The list of cities to fetch weather data for
    cities = ["London", "New York", "Tokyo", "Paris", "Sydney", "Berlin", "Dubai"]
    
    logger.info("=" * 100)
    logger.info("🌍 WEATHER DATA ANALYZER - START")
    logger.info("=" * 100)
    logger.info(f"Cities to analyze: {', '.join(cities)}")
    
    try:
        logger.info("Starting weather data processing...")
        df = get_weather_data_for_cities(cities, "weather_data.csv")
        logger.info("✅ Weather data processing completed successfully!")
    except Exception as e:
        logger.error(f"❌ Error during processing: {str(e)}", exc_info=True)
    finally:
        logger.info("=" * 100)
        logger.info("🌍 WEATHER DATA ANALYZER - END")
        logger.info("=" * 100)
