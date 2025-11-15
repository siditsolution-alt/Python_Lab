import pandas as pd
import os
from datetime import datetime
from weather_logger import get_logger

logger = get_logger()

def convert_to_dataframe(weather_records):
    """
    Convert weather records to a Pandas DataFrame.
    
    Args:
        weather_records (list): List of weather record dictionaries
        
    Returns:
        pd.DataFrame: DataFrame containing weather data
    """
    df = pd.DataFrame(weather_records)
    logger.info("Weather data converted to DataFrame")
    
    return df

def inspect_dataframe(df):
    """
    Inspect and display DataFrame information.
    
    Args:
        df (pd.DataFrame): DataFrame to inspect
    """
    logger.info("=" * 60)
    logger.info("DATAFRAME INSPECTION")
    logger.info("=" * 60)
    
    # Display shape
    logger.info(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Display column names and data types
    logger.info("\nColumn Information:")
    for col in df.columns:
        logger.info(f"  - {col}: {df[col].dtype}")
    
    # Display first few rows
    logger.info("\nFirst few rows:")
    logger.info(f"\n{df.head()}")
    
    # Display summary statistics
    logger.info("\nData Summary:")
    logger.info(f"\n{df.describe()}")
    
    logger.info("=" * 60)

def save_to_csv(df, output_file="weather_data.csv"):
    """
    Save DataFrame to CSV file in the Output folder (outside Weather_Data_Analyzer).
    
    Args:
        df (pd.DataFrame): DataFrame to save
        output_file (str): Name of the output CSV file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Join the output directory with the filename
        output_path = os.path.join(output_dir, output_file)
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"Weather data successfully saved to {output_path}")
        logger.info(f"File contains {len(df)} rows and {len(df.columns)} columns")
        return True
        
    except IOError as e:
        logger.error(f"Error writing CSV file: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving CSV: {e}")
        return False