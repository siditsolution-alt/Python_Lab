import numpy as np
import pandas as pd
from datetime import datetime
from weather_logger import get_logger

logger = get_logger()


def calculate_temperature_statistics(temperature_records):
    """
    Calculate statistics (average, max, min) for temperatures using NumPy.
    
    Args:
        temperature_records (list): List of records containing temperature data
        
    Returns:
        dict: Dictionary containing calculated statistics
    """
    # Extract temperature values in Celsius
    temp_values = np.array([
        record['temperature_c'] for record in temperature_records
        if record['temperature_c'] is not None
    ])
    
    if len(temp_values) == 0:
        logger.warning("No valid temperature data available for statistics")
        return None
    
    stats = {
        'average': np.mean(temp_values),
        'median': np.median(temp_values),
        'max': np.max(temp_values),
        'min': np.min(temp_values),
        'std_dev': np.std(temp_values),
        'variance': np.var(temp_values),
        'range': np.max(temp_values) - np.min(temp_values),
        'percentile_25': np.percentile(temp_values, 25),
        'percentile_75': np.percentile(temp_values, 75)
    }
    
    return stats

def identify_temperature_patterns(temperature_records, cities):
    """
    Identify patterns and trends in temperature data.
    
    Args:
        temperature_records (list): List of records containing temperature data
        cities (list): List of city names
        
    Returns:
        dict: Dictionary containing identified patterns
    """
    patterns = {}
    
    # Create a mapping of city to temperature data
    city_temp_map = {record['city']: record['temperature_c'] for record in temperature_records}
    
    # Extract temperature values and city names
    temp_values = np.array([
        city_temp_map[city] for city in cities 
        if city in city_temp_map and city_temp_map[city] is not None
    ])
    
    city_names = np.array([
        city for city in cities 
        if city in city_temp_map and city_temp_map[city] is not None
    ])
    
    # Identify hottest and coldest cities
    if len(temp_values) > 0:
        max_temp_idx = np.argmax(temp_values)
        min_temp_idx = np.argmin(temp_values)
        
        patterns['hottest_city'] = city_names[max_temp_idx]
        patterns['hottest_temp'] = temp_values[max_temp_idx]
        
        patterns['coldest_city'] = city_names[min_temp_idx]
        patterns['coldest_temp'] = temp_values[min_temp_idx]
        
        # Calculate temperature anomalies (deviation from mean)
        mean_temp = np.mean(temp_values)
        anomalies = temp_values - mean_temp
        
        patterns['temperature_anomalies'] = {
            city: anomaly for city, anomaly in zip(city_names, anomalies)
        }
        
        # Identify temperature zones
        patterns['temperature_zones'] = {
            'hot': np.sum(temp_values > mean_temp + np.std(temp_values)),
            'moderate': np.sum(np.abs(temp_values - mean_temp) <= np.std(temp_values)),
            'cold': np.sum(temp_values < mean_temp - np.std(temp_values))
        }
    
    return patterns


def analyze_humidity_correlation(temperature_records):
    """
    Analyze correlation between temperature and humidity using NumPy.
    
    Args:
        temperature_records (list): List of records containing temperature and humidity data
        
    Returns:
        dict: Correlation analysis results
    """
    temp_values = np.array([
        record['temperature_c'] for record in temperature_records
        if record['temperature_c'] is not None
    ])
    
    humidity_values = np.array([
        record['humidity'] for record in temperature_records
        if record['humidity'] is not None
    ])
    
    correlation_data = {}
    
    if len(temp_values) > 1 and len(humidity_values) > 1:
        # Calculate correlation coefficient
        correlation = np.corrcoef(temp_values, humidity_values)[0, 1]
        correlation_data['correlation_coefficient'] = correlation
        
        if np.isnan(correlation):
            correlation_data['correlation_interpretation'] = "Insufficient data for correlation"
        elif correlation > 0.5:
            correlation_data['correlation_interpretation'] = "Strong positive correlation"
        elif correlation > 0:
            correlation_data['correlation_interpretation'] = "Weak positive correlation"
        elif correlation > -0.5:
            correlation_data['correlation_interpretation'] = "Weak negative correlation"
        else:
            correlation_data['correlation_interpretation'] = "Strong negative correlation"
    
    return correlation_data


def display_analysis_results(stats, patterns, correlation=None):
    """
    Display all analysis results in a formatted manner.
    
    Args:
        stats (dict): Temperature statistics
        patterns (dict): Identified patterns
    """
    logger.info("=" * 70)
    logger.info("TEMPERATURE ANALYSIS REPORT")
    logger.info("=" * 70)
    
    if stats:
        logger.info("\n📊 TEMPERATURE STATISTICS (Celsius)")
        logger.info("-" * 70)
        logger.info(f"  Average Temperature:        {stats['average']:.2f}°C")
        logger.info(f"  Median Temperature:         {stats['median']:.2f}°C")
        logger.info(f"  Maximum Temperature:        {stats['max']:.2f}°C")
        logger.info(f"  Minimum Temperature:        {stats['min']:.2f}°C")
        logger.info(f"  Temperature Range:          {stats['range']:.2f}°C")
        logger.info(f"  Standard Deviation:         {stats['std_dev']:.2f}°C")
        logger.info(f"  Variance:                   {stats['variance']:.2f}")
        logger.info(f"  25th Percentile:            {stats['percentile_25']:.2f}°C")
        logger.info(f"  75th Percentile:            {stats['percentile_75']:.2f}°C")
    
    if patterns:
        logger.info("\n🌡️ TEMPERATURE PATTERNS & TRENDS")
        logger.info("-" * 70)
        logger.info(f"  Hottest City:               {patterns['hottest_city']} ({patterns['hottest_temp']:.2f}°C)")
        logger.info(f"  Coldest City:               {patterns['coldest_city']} ({patterns['coldest_temp']:.2f}°C)")
        
        logger.info("\n  Temperature Zones:")
        zones = patterns['temperature_zones']
        logger.info(f"    - Hot cities:             {zones['hot']}")
        logger.info(f"    - Moderate cities:        {zones['moderate']}")
        logger.info(f"    - Cold cities:            {zones['cold']}")
        
        logger.info("\n  Temperature Anomalies (deviation from mean):")
        for city, anomaly in patterns['temperature_anomalies'].items():
            symbol = "🔥" if anomaly > 0 else "❄️"
            logger.info(f"    {symbol} {city:15} {anomaly:+.2f}°C")
    
    if correlation and 'correlation_coefficient' in correlation:
        logger.info("\n🔗 TEMPERATURE-HUMIDITY CORRELATION")
        logger.info("-" * 70)
        logger.info(f"  Correlation Coefficient:    {correlation['correlation_coefficient']:.4f}")
        logger.info(f"  Interpretation:             {correlation['correlation_interpretation']}")
    
    logger.info("=" * 70)


def analyze_weather_data(temperature_records, cities):
    """
    Main function to perform complete temperature analysis.
    
    Args:
        temperature_records (list): List of records containing temperature data
        cities (list): List of city names to analyze
    """   
    logger.info("🌍 Starting comprehensive weather analysis...")
    
    # Calculate statistics
    stats = calculate_temperature_statistics(temperature_records)
    
    # Identify patterns
    patterns = identify_temperature_patterns(temperature_records, cities)
    
    # Analyze correlation
    correlation = analyze_humidity_correlation(temperature_records)
        
    # Display results
    display_analysis_results(stats, patterns, correlation)
    
    return stats


