"""
Weather Data Analyzer - Web UI
Flask application to display weather charts
"""

from flask import Flask, render_template, send_from_directory, jsonify
import os
from pathlib import Path
from glob import glob
import sys

# Get parent directory (outside Weather_Data_Analyzer)
parent_dir = os.path.dirname(os.path.dirname(__file__))
output_dir = os.path.join(parent_dir, 'Output')
charts_dir = os.path.join(output_dir, 'charts')

# Create Flask app
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(parent_dir, 'Output'))

def get_latest_charts():
    """
    Get the latest chart files from the charts directory.
    
    Returns:
        dict: Dictionary with chart types as keys and file paths as values
    """
    charts = {
        'dashboard': None,
        'temperature_comparison': None,
        'humidity_distribution': None,
        'temp_humidity_scatter': None,
        'weather_conditions': None
    }
    
    if not os.path.exists(charts_dir):
        return charts
    
    # Pattern for each chart type
    patterns = {
        'dashboard': 'weather_dashboard_*.png',
        'temperature_comparison': 'temperature_comparison_*.png',
        'humidity_distribution': 'humidity_distribution_*.png',
        'temp_humidity_scatter': 'temp_humidity_scatter_*.png',
        'weather_conditions': 'weather_conditions_*.png'
    }
    
    for chart_type, pattern in patterns.items():
        files = glob(os.path.join(charts_dir, pattern))
        if files:
            # Get the most recent file
            latest_file = max(files, key=os.path.getctime)
            # Get relative path for serving
            charts[chart_type] = os.path.basename(latest_file)
    
    return charts

@app.route('/')
def index():
    """Main page displaying all weather charts."""
    charts = get_latest_charts()
    return render_template('index.html', charts=charts)

@app.route('/charts/<filename>')
def serve_chart(filename):
    """Serve chart images from the charts directory."""
    return send_from_directory(charts_dir, filename)

@app.route('/api/charts')
def api_charts():
    """API endpoint to get latest charts."""
    charts = get_latest_charts()
    # Convert to URLs
    chart_urls = {}
    for chart_type, filename in charts.items():
        if filename:
            chart_urls[chart_type] = f"/charts/{filename}"
        else:
            chart_urls[chart_type] = None
    return jsonify(chart_urls)

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to refresh charts (triggers data fetch)."""
    # This could trigger a background job to fetch new data
    # For now, just return success
    return jsonify({"status": "success", "message": "Charts refreshed"})

if __name__ == '__main__':
    # Create charts directory if it doesn't exist
    os.makedirs(charts_dir, exist_ok=True)
    
    print("=" * 60)
    print("🌍 Weather Data Analyzer - Web UI")
    print("=" * 60)
    print(f"📁 Charts directory: {charts_dir}")
    print(f"🌐 Starting server on http://127.0.0.1:5000")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print()
    
    # Disable reloader to avoid path issues when run from run_ui.py
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
