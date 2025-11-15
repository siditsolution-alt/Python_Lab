# Weather Data Analyzer

A comprehensive Python application for fetching, analyzing, and visualizing weather data from multiple cities. Features include data processing with Pandas, statistical analysis with NumPy, chart generation with Matplotlib, and an interactive web-based dashboard using Flask.

## 🌟 Features

- 🌍 **Multi-City Weather Data Fetching**: Fetch weather data for multiple cities simultaneously using WeatherAPI
- 📊 **Data Analysis**: Statistical analysis using NumPy (mean, median, standard deviation, correlation analysis)
- 📈 **Chart Generation**: Automatic generation of multiple chart types:
  - Weather Dashboard (temperature & humidity overview)
  - Temperature Comparison (bar chart)
  - Humidity Distribution (horizontal bar chart)
  - Temperature vs Humidity Scatter Plot
  - Weather Conditions Distribution
- 🖥️ **Web UI Dashboard**: Interactive web-based dashboard to view all charts in a browser
- 💾 **CSV Export**: Export weather data to CSV files with timestamps
- 📝 **Comprehensive Logging**: Detailed logging system for debugging and monitoring
- 🎨 **Beautiful Visualizations**: High-quality charts with color-coded temperature ranges
- 📱 **Responsive Design**: Web UI works on desktop, tablet, and mobile devices

## 📁 Project Structure

```
Weather_Data_Analyzer/
├── 📄 run.py                                    # Main entry point (CLI mode)
├── 📄 run_ui.py                                 # Web UI launcher
├── 📄 run.bat                                   # Windows batch file for CLI
├── 📄 run_ui.bat                                # Windows batch file for Web UI
├── 📁 Weather_Data_Analyzer/
│   ├── 📄 .env                                  # Environment variables (API keys)
│   ├── 📄 main.py                               # Core application logic
│   ├── 📄 requirments.txt                      # Python dependencies
│   ├── 📄 weather_api_service.py               # WeatherAPI integration
│   ├── 📄 weather_data_service.py              # Main data processing orchestrator
│   ├── 📄 weather_logger.py                    # Logging configuration
│   ├── 📄 weather_matplotlib_graph_generator.py # Chart generation with Matplotlib
│   ├── 📄 weather_numpy_analyzer.py            # Statistical analysis with NumPy
│   ├── 📄 weather_panda_data_handler.py        # Data processing with Pandas
│   ├── 📄 weather_ui.py                        # Flask web application
│   └── 📁 templates/
│       └── 📄 index.html                       # Web UI template
└── 📁 Output/                                   # Generated files (created at runtime)
    ├── 📁 charts/                               # Generated chart images
    ├── 📁 csv/                                  # Exported CSV files
    └── 📁 logs/                                 # Application logs
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- WeatherAPI account (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Weather_Data_Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r Weather_Data_Analyzer/requirments.txt
   ```

3. **Set up API key**
   - Get a free API key from [WeatherAPI](https://www.weatherapi.com/)
   - Update the `WEATHER_API_KEY` in `Weather_Data_Analyzer/.env`

### Running the Application

#### Option 1: Command Line Interface (CLI)
```bash
# Using Python
python run.py

# Using Windows batch file
run.bat
```

#### Option 2: Web Dashboard
```bash
# Using Python
python run_ui.py

# Using Windows batch file
run_ui.bat
```

The web dashboard will be available at `http://127.0.0.1:5000`

## 📊 Default Cities

The application analyzes weather data for these cities by default:
- London 🇬🇧
- New York 🇺🇸
- Tokyo 🇯🇵
- Paris 🇫🇷
- Sydney 🇦🇺
- Berlin 🇩🇪
- Dubai 🇦🇪

You can modify the city list in `Weather_Data_Analyzer/main.py`.

## 📈 Generated Charts

The application creates the following visualizations:

1. **Weather Dashboard** - Overview of temperature and humidity for all cities
2. **Temperature Comparison** - Bar chart comparing temperatures across cities
3. **Humidity Distribution** - Horizontal bar chart of humidity levels
4. **Temperature vs Humidity Scatter Plot** - Correlation analysis
5. **Weather Conditions Distribution** - Pie chart of weather conditions

All charts are saved as high-resolution PNG files in the `Output/charts/` directory.

## 💾 Data Export

- **CSV Files**: Weather data is exported to timestamped CSV files in `Output/csv/`
- **Logs**: Detailed application logs are saved in `Output/logs/`

## 🔧 Configuration

### Environment Variables (.env)
```env
WEATHER_API_KEY="your_api_key_here"
WEATHER_API_BASE_URL="http://api.weatherapi.com/v1"
```

### Dependencies (requirments.txt)
- `requests>=2.28.0` - HTTP requests for API calls
- `numpy>=1.24.0` - Statistical analysis
- `pandas>=1.5.0` - Data manipulation
- `matplotlib>=3.7.0` - Chart generation
- `python-dotenv>=0.21.0` - Environment variable management
- `flask>=2.3.0` - Web framework for UI

## 🏗️ Architecture

### Core Components

1. **weather_api_service.py** - Handles WeatherAPI integration and data fetching
2. **weather_panda_data_handler.py** - Processes raw data using Pandas
3. **weather_numpy_analyzer.py** - Performs statistical analysis using NumPy
4. **weather_matplotlib_graph_generator.py** - Creates visualizations with Matplotlib
5. **weather_data_service.py** - Orchestrates the entire data pipeline
6. **weather_ui.py** - Flask web application for interactive dashboard
7. **weather_logger.py** - Centralized logging system

### Data Flow

```
API Request → Data Fetching → Pandas Processing → NumPy Analysis → Matplotlib Charts → Web UI Display
```

## 🌐 Web UI Features

- **Real-time Chart Display** - View all generated charts in your browser
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Auto-refresh** - Charts update when new data is processed
- **Chart Navigation** - Easy switching between different visualizations

## 📝 Logging

The application provides comprehensive logging:
- **INFO**: General application flow and status updates
- **ERROR**: Error conditions with stack traces
- **DEBUG**: Detailed debugging information (when enabled)

Logs are saved to `Output/logs/weather_analyzer_YYYYMMDD_HHMMSS.log`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your WeatherAPI key is valid and set in `.env`
2. **Module Not Found**: Install dependencies with `pip install -r Weather_Data_Analyzer/requirments.txt`
3. **Permission Errors**: Ensure the application has write permissions for the `Output/` directory
4. **Port Already in Use**: The web UI uses port 5000 by default. Close other applications using this port.

### Getting Help

- Check the logs in `Output/logs/` for detailed error information
- Ensure all dependencies are installed correctly
- Verify your internet connection for API requests