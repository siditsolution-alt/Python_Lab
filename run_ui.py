#!/usr/bin/env python3
"""
Weather Data Analyzer - Web UI Launcher
Run this script to start the web UI server.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located (project root)
    project_root = Path(__file__).parent.absolute()
    weather_analyzer_dir = project_root / "Weather_Data_Analyzer"
    weather_ui_script = weather_analyzer_dir / "weather_ui.py"
    
    if not weather_ui_script.exists():
        print(f"❌ Error: {weather_ui_script} not found")
        sys.exit(1)
    
    print("=" * 60)
    print("🌍 Weather Data Analyzer - Web UI")
    print("=" * 60)
    print(f"📍 Project root: {project_root}")
    print(f"📁 Charts directory: {project_root / 'Output' / 'charts'}")
    print(f"🌐 Starting server on http://127.0.0.1:5000")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print()
    
    # Run the Flask app directly using Python
    # This avoids reloader issues by running it as a subprocess
    try:
        # Change to the Weather_Data_Analyzer directory
        os.chdir(weather_analyzer_dir)
        # Run the Flask app
        subprocess.run([sys.executable, "weather_ui.py"], check=True)
    except KeyboardInterrupt:
        print("\n⚠️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
