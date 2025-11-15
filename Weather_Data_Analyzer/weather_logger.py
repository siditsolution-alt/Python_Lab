import logging
import os
from datetime import datetime

def setup_logging(log_dir=None, log_filename=None):
    """
    Set up centralized logging for the Weather Data Analyzer project.
    
    Args:
        log_dir (str): Directory to store log files (default: Output/logs in parent directory)
        log_filename (str): Specific log filename (default: weather_analyzer_YYYYMMDD.log)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if log_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        log_directory = os.path.join(parent_dir, 'Output', 'logs')
    else:
        log_directory = os.path.join(os.path.dirname(__file__), log_dir)
    
    os.makedirs(log_directory, exist_ok=True)
    
    # Set log filename with date and time if not provided
    if log_filename is None:
        datetime_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"weather_analyzer_{datetime_str}.log"
    
    log_filepath = os.path.join(log_directory, log_filename)
    
    # Create logger
    logger = logging.getLogger('WeatherAnalyzer')
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (logs everything)
    file_handler = logging.FileHandler(log_filepath, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler (logs INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Log initialization message
    logger.info(f"Logging initialized - Log file: {log_filepath}")
    
    return logger


def get_logger():
    """
    Get the configured logger instance.
    
    Returns:
        logging.Logger: Configured logger
    """
    return logging.getLogger('WeatherAnalyzer')
