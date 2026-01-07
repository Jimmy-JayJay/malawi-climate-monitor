from datetime import datetime

# --- Simulated 30-Year Climatology (1991-2020) for Malawi ---
# Monthly averages (deg C) for our key cities
CLIMATOLOGY = {
    "Lilongwe": [23.0, 23.2, 22.8, 21.5, 19.8, 17.6, 17.2, 19.5, 22.8, 24.8, 25.2, 23.5],
    "Blantyre": [24.0, 24.2, 23.8, 22.5, 20.8, 18.6, 18.2, 20.5, 23.8, 25.8, 26.2, 24.5],
    "Mzuzu":    [20.0, 20.2, 20.8, 19.5, 17.8, 15.6, 15.2, 17.5, 20.8, 22.8, 23.2, 21.5],
    "Zomba":    [23.5, 23.7, 23.3, 22.0, 20.3, 18.1, 17.7, 20.0, 23.3, 25.3, 25.7, 24.0]
}

def get_anomaly(city, current_temp):
    """Calculates temperature anomaly vs 30-year operational baseline."""
    # Get current month (0-11 index)
    current_month_idx = datetime.now().month - 1
    
    # Get baseline for this city/month
    baseline = CLIMATOLOGY.get(city, CLIMATOLOGY["Lilongwe"])[current_month_idx]
    
    anomaly = current_temp - baseline
    return round(anomaly, 1), baseline

def calculate_heat_risk(temp, humidity):
    """
    Calculates Heat Risk based on simplified Heat Index logic.
    Returns: (Risk Level, Color Code)
    """
    # Very simplified approximation for educational purposes
    # High humidity amplifies heat feeling
    heat_index = temp + 0.05 * humidity
    
    if heat_index < 27:
        return "Safe", "text-emerald-400"
    elif 27 <= heat_index < 32:
        return "Caution", "text-yellow-400"
    elif 32 <= heat_index < 41:
        return "Extreme Caution", "text-orange-400"
    elif 41 <= heat_index < 54:
        return "Danger", "text-red-500"
    else:
        return "Extreme Danger", "text-purple-500"
