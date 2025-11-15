#!/usr/bin/env python3
"""
Weather Data Analyzer - Main Entry Point
Run this script from the project root to execute the Weather Data Analyzer.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the directory where this script is located (project root)
    project_root = Path(__file__).parent.absolute()
    weather_analyzer_dir = project_root / "Weather_Data_Analyzer"
    main_script = weather_analyzer_dir / "main.py"
    
    # Validate paths
    if not weather_analyzer_dir.exists():
        print(f"❌ Error: Weather_Data_Analyzer directory not found at {weather_analyzer_dir}")
        print(f"   Current directory: {project_root}")
        sys.exit(1)
    
    if not main_script.exists():
        print(f"❌ Error: main.py not found at {main_script}")
        sys.exit(1)
    
    # Change to Weather_Data_Analyzer directory (so relative imports work)
    os.chdir(weather_analyzer_dir)
    
    # Run main.py using the same Python interpreter
    print(f"📍 Running from: {weather_analyzer_dir}")
    print(f"🐍 Python: {sys.executable}")
    print()
    
    try:
        result = subprocess.run([sys.executable, "main.py"], check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error executing main.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
