import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import os
from datetime import datetime
from weather_logger import get_logger

logger = get_logger()


def get_temp_color(temp):
    """
    Get color for temperature value.
    
    Args:
        temp (float): Temperature in Celsius
        
    Returns:
        str: Color code
    """
    if temp > 30:
        return '#FF4444'  # Dark red
    elif temp > 20:
        return '#FF8C00'  # Orange
    elif temp > 10:
        return '#4ECDC4'  # Teal
    else:
        return '#3498DB'  # Blue


def create_summary_table(temperature_records, cities):
    """
    Create a comprehensive summary table from temperature records.
    
    Args:
        temperature_records (list): List of records containing temperature data
        cities (list): List of city names
        
    Returns:
        pd.DataFrame: Summary table with all weather data
    """
    summary_data = []
    
    for record in temperature_records:
        summary_data.append({
            'City': record['city'],
            'Temp (°C)': record['temperature_c'],
            'Temp (°F)': record['temperature_f'],
            'Humidity (%)': record['humidity'],
            'Condition': record['condition']
        })
    
    df_summary = pd.DataFrame(summary_data)
    return df_summary


def display_summary_table(df_summary):
    """
    Display the summary table in a formatted manner.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
    """
    logger.info("\n" + "=" * 100)
    logger.info("WEATHER DATA SUMMARY TABLE")
    logger.info("=" * 100)
    
    # Format the table for display
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    logger.info(f"\n{df_summary.to_string(index=False)}")
    logger.info("\n" + "=" * 100)


def generate_simple_dashboard(temperature_records, cities, output_dir=None):
    """
    Generate a simple dashboard with line graphs for temperature and humidity.
    
    Args:
        temperature_records (list): List of records containing temperature data
        cities (list): List of city names
        output_dir (str): Output directory for charts (default: Output/charts in parent directory)
    """
    # Set default output directory
    if output_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output', 'charts')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data
    temps = np.array([record['temperature_c'] for record in temperature_records if record['temperature_c'] is not None])
    humidities = np.array([record['humidity'] for record in temperature_records if record['humidity'] is not None])
    cities_filtered = [record['city'] for record in temperature_records if record['temperature_c'] is not None]
    
    if len(temps) == 0:
        logger.warning("No temperature data available for dashboard")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    x_positions = np.arange(len(cities_filtered))
    
    # Plot temperature line
    ax.plot(x_positions, temps, marker='o', linestyle='-', color='red', 
            linewidth=2.5, markersize=10, label='Temperature (°C)', zorder=3)
    
    # Plot humidity line
    ax.plot(x_positions, humidities, marker='s', linestyle='--', color='blue', 
            linewidth=2.5, markersize=10, label='Humidity (%)', zorder=3)
    
    # Add temperature and humidity text labels at each point
    for i, city in enumerate(cities_filtered):
        # Temperature text
        ax.text(x_positions[i], temps[i] + 3, f"{temps[i]:.1f}°C", 
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='red')
        
        # Humidity text
        ax.text(x_positions[i], humidities[i] - 3, f"{humidities[i]:.0f}%", 
                ha='center', va='top', fontsize=10, fontweight='bold', color='blue')
    
    # Add average lines
    avg_temp = np.mean(temps)
    avg_humidity = np.mean(humidities)
    
    ax.axhline(avg_temp, color='red', linestyle=':', linewidth=2, alpha=0.7, 
               label=f'Avg Temp: {avg_temp:.1f}°C')
    ax.axhline(avg_humidity, color='blue', linestyle=':', linewidth=2, alpha=0.7, 
               label=f'Avg Humidity: {avg_humidity:.1f}%')
    
    # Styling
    ax.set_xlabel('Cities', fontsize=13, fontweight='bold')
    ax.set_ylabel('Temperature (°C) / Humidity (%)', fontsize=13, fontweight='bold')
    ax.set_title('🌍 City-wise Temperature & Humidity Overview', fontsize=16, fontweight='bold', pad=20)
    
    # Set x-axis ticks and labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(cities_filtered, rotation=45, ha='right', fontsize=11)
    
    # Grid and legend
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
    
    # Set y-axis limits for better spacing
    y_min = min(min(temps), min(humidities)) - 5
    y_max = max(max(temps), max(humidities)) + 10
    ax.set_ylim(y_min, y_max)
    
    plt.tight_layout()
    
    # Save with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"weather_dashboard_{timestamp}.png")
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"✅ Main dashboard saved to {output_file}")
    plt.close()


def create_temperature_comparison_chart(df_summary, output_dir=None):
    """
    Create a bar chart comparing temperatures across cities.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
        output_dir (str): Output directory for charts (default: Output/charts in parent directory)
    """
    # Set default output directory
    if output_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output', 'charts')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    cities = df_summary['City']
    temps_c = df_summary['Temp (°C)']
    
    # Create color map based on temperature ranges
    colors = [get_temp_color(temp) for temp in temps_c]
    
    bars = ax.bar(cities, temps_c, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}°C',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('City', fontsize=12, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_title('Temperature Comparison Across Cities', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"temperature_comparison_{timestamp}.png"), dpi=300, bbox_inches='tight')
    logger.info(f"✅ Temperature comparison chart saved")
    plt.close()


def create_humidity_distribution_chart(df_summary, output_dir=None):
    """
    Create a horizontal bar chart showing humidity levels by city.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
        output_dir (str): Output directory for charts (default: Output/charts in parent directory)
    """
    # Set default output directory
    if output_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output', 'charts')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    humidity = df_summary['Humidity (%)'].dropna()
    
    ax.barh(df_summary['City'], humidity, color='#87CEEB', edgecolor='black', linewidth=1.5, alpha=0.8)
    
    for i, val in enumerate(humidity):
        ax.text(val + 1, i, f'{val:.0f}%', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Humidity (%)', fontsize=12, fontweight='bold')
    ax.set_title('Humidity Levels by City', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"humidity_distribution_{timestamp}.png"), dpi=300, bbox_inches='tight')
    logger.info(f"✅ Humidity distribution chart saved")
    plt.close()


def create_temperature_humidity_scatter(df_summary, output_dir=None):
    """
    Create a scatter plot showing relationship between temperature and humidity.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
        output_dir (str): Output directory for charts (default: Output/charts in parent directory)
    """
    # Set default output directory
    if output_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output', 'charts')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fig, ax = plt.subplots(figsize=(10, 7))
    
    temps = df_summary['Temp (°C)'].dropna()
    humidity = df_summary['Humidity (%)'].dropna()
    cities = df_summary['City'][:len(temps)]
    
    scatter = ax.scatter(temps, humidity, s=300, alpha=0.6, c=temps, cmap='RdYlBu_r', 
                         edgecolors='black', linewidth=2)
    
    # Add city labels to points
    for i, city in enumerate(cities):
        if i < len(temps) and i < len(humidity):
            ax.annotate(city, (temps.iloc[i], humidity.iloc[i]), 
                       ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Humidity (%)', fontsize=12, fontweight='bold')
    ax.set_title('Temperature vs Humidity Relationship', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Temperature (°C)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"temp_humidity_scatter_{timestamp}.png"), dpi=300, bbox_inches='tight')
    logger.info(f"✅ Temperature-Humidity scatter plot saved")
    plt.close()


def create_weather_conditions_chart(df_summary, output_dir=None):
    """
    Create a bar chart showing weather condition distribution.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
        output_dir (str): Output directory for charts (default: Output/charts in parent directory)
    """
    # Set default output directory
    if output_dir is None:
        # Get parent directory (outside Weather_Data_Analyzer)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        output_dir = os.path.join(parent_dir, 'Output', 'charts')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    conditions = df_summary['Condition'].value_counts()
    
    colors_conditions = ['#FFD700', '#87CEEB', '#808080', '#FF6B6B', '#90EE90']
    bars = ax.barh(conditions.index, conditions.values, color=colors_conditions[:len(conditions)], 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2., f' {int(width)}',
               ha='left', va='center', fontweight='bold', fontsize=11)
    
    ax.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax.set_ylabel('Weather Condition', fontsize=12, fontweight='bold')
    ax.set_title('Weather Conditions Distribution', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"weather_conditions_{timestamp}.png"), dpi=300, bbox_inches='tight')
    logger.info(f"✅ Weather conditions chart saved")
    plt.close()


def generate_insights(df_summary, stats):
    """
    Generate textual insights from the data.
    
    Args:
        df_summary (pd.DataFrame): Summary DataFrame
        stats (dict): Statistics from NumPy analysis
        
    Returns:
        str: Formatted insights text
    """
    insights = []
    
    insights.append("\n" + "=" * 100)
    insights.append("KEY INSIGHTS & FINDINGS")
    insights.append("=" * 100)
    
    if stats:
        insights.append(f"\n📊 TEMPERATURE INSIGHTS:")
        insights.append(f"  • Global Average Temperature: {stats['average']:.2f}°C")
        insights.append(f"  • Highest Temperature: {stats['max']:.2f}°C")
        insights.append(f"  • Lowest Temperature: {stats['min']:.2f}°C")
        insights.append(f"  • Temperature Variation: {stats['range']:.2f}°C")
        insights.append(f"  • Temperature Stability (Std Dev): {stats['std_dev']:.2f}°C")
    
    # Humidity insights
    avg_humidity = df_summary['Humidity (%)'].mean()
    max_humidity = df_summary['Humidity (%)'].max()
    min_humidity = df_summary['Humidity (%)'].min()
    
    insights.append(f"\n💧 HUMIDITY INSIGHTS:")
    insights.append(f"  • Average Humidity: {avg_humidity:.1f}%")
    insights.append(f"  • Highest Humidity: {max_humidity:.1f}%")
    insights.append(f"  • Lowest Humidity: {min_humidity:.1f}%")
    
    # Weather conditions insights
    condition_counts = df_summary['Condition'].value_counts()
    most_common = condition_counts.index[0]
    most_common_count = condition_counts.values[0]
    
    insights.append(f"\n🌤️ WEATHER CONDITIONS:")
    insights.append(f"  • Most Common Condition: {most_common} ({most_common_count} cities)")
    insights.append(f"  • Weather Diversity: {len(condition_counts)} different conditions observed")
    
    insights.append(f"\n📍 CITY STATISTICS:")
    insights.append(f"  • Total Cities Analyzed: {len(df_summary)}")
    
    insights.append("\n" + "=" * 100 + "\n")
    
    return "\n".join(insights)


def generate_graphs(temperature_records, cities, stats):
    """
    Main function to create a comprehensive dashboard with summary and visualizations.
    
    Args:
        temperature_records (list): List of temperature records
        cities (list): List of city names
        stats (dict): Statistics from NumPy analysis
    """
    logger.info("🎨 Creating weather dashboard...")
    
    # Set up output directory (Output/charts in parent directory)
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(parent_dir, 'Output', 'charts')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary table
    df_summary = create_summary_table(temperature_records, cities)
    
    # Display summary table
    display_summary_table(df_summary)
    
    # Generate insights
    insights_text = generate_insights(df_summary, stats)
    logger.info(insights_text)
    
    # Create main simple dashboard with line graphs
    logger.info("📈 Generating main dashboard...")
    generate_simple_dashboard(temperature_records, cities, output_dir)
    
    # Create detailed charts
    logger.info("📊 Generating detailed charts...")
    create_temperature_comparison_chart(df_summary, output_dir)
    create_humidity_distribution_chart(df_summary, output_dir)
    create_temperature_humidity_scatter(df_summary, output_dir)
    create_weather_conditions_chart(df_summary, output_dir)
    
    logger.info("\n✅ Dashboard creation completed!")
    logger.info(f"📁 All charts saved in: {output_dir}")
    
    return df_summary
