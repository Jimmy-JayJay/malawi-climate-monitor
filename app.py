from flask import Flask, render_template, request, send_file
import requests
from datetime import datetime
import folium
import os
from backend.analytics import get_anomaly, calculate_heat_risk
from fpdf import FPDF

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LOCATIONS = {
    "Lilongwe": {"lat": -13.98, "lon": 33.78},
    "Blantyre": {"lat": -15.79, "lon": 35.00},
    "Mzuzu": {"lat": -11.46, "lon": 34.02},
    "Zomba": {"lat": -15.38, "lon": 35.32}
}

def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def get_forecast(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        
        # Process: Get one reading per day (e.g., closest to noon)
        # The API returns 3-hour steps.
        daily_forecast = []
        seen_dates = set()
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            
            # Simple logic: take the first entry for each unique date (or noon if we wanted to be fancy)
            # Since we want next days, skip today if needed, or simple take distinct dates.
            if date_str not in seen_dates:
                seen_dates.add(date_str)
                daily_forecast.append({
                    "date": dt.strftime('%a, %d %b'),
                    "temp": item['main']['temp'],
                    "condition": item['weather'][0]['main'],
                    "icon": item['weather'][0]['icon'],
                    "timestamp": dt.strftime('%H:%M') # For the chart
                })
                
        # Also return raw list for the chart (first 8-10 items for detail)
        chart_data = {
            "labels": [datetime.fromtimestamp(x['dt']).strftime('%H:%M') for x in data['list'][:8]],
            "temps": [x['main']['temp'] for x in data['list'][:8]]
        }
                
        return daily_forecast[:5], chart_data
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return [], {"labels": [], "temps": []}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_city = "Lilongwe"
    if request.method == "POST":
        selected_city = request.form.get("city")
    
    coords = LOCATIONS.get(selected_city, LOCATIONS["Lilongwe"])
    weather_data = get_weather(coords["lat"], coords["lon"])
    forecast_data, chart_data = get_forecast(coords["lat"], coords["lon"])
    
    # Climate Analytics
    anomaly, baseline = get_anomaly(selected_city, weather_data['main']['temp'])
    risk_level, risk_color = calculate_heat_risk(weather_data['main']['temp'], weather_data['main']['humidity'])
    
    # Generate Map
    m = folium.Map(location=[coords["lat"], coords["lon"]], zoom_start=10)
    folium.Marker(
        [coords["lat"], coords["lon"]], 
        popup=f"{selected_city}: {weather_data['main']['temp']}°C",
        icon=folium.Icon(color="red" if anomaly > 0 else "blue")
    ).add_to(m)
    map_html = m._repr_html_()

    current_date = datetime.now().strftime("%A, %d %B %Y")
    
    return render_template("index.html", 
                           weather=weather_data, 
                           forecast=forecast_data,
                           chart_data=chart_data,
                           city=selected_city, 
                           cities=LOCATIONS.keys(),
                           date=current_date,
                           anomaly=anomaly,
                           baseline=baseline,
                           risk_level=risk_level,
                           risk_color=risk_color,
                           map_html=map_html)

@app.route("/report")
def download_report():
    # PDF Agent (Simple)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Malawi National Climate Bulletin", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 10, "Station", 1)
    pdf.cell(30, 10, "Temp (C)", 1)
    pdf.cell(30, 10, "Humidity", 1)
    pdf.cell(30, 10, "Anomaly", 1)
    pdf.cell(40, 10, "Risk Level", 1)
    pdf.ln()

    # Table Body
    pdf.set_font("Arial", '', 10)
    
    for city, coords in LOCATIONS.items():
        data = get_weather(coords["lat"], coords["lon"])
        if data:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            anomaly, base = get_anomaly(city, temp)
            risk, _ = calculate_heat_risk(temp, humidity)
            
            pdf.cell(30, 10, city, 1)
            pdf.cell(30, 10, f"{temp:.1f}", 1)
            pdf.cell(30, 10, f"{humidity}%", 1)
            pdf.cell(30, 10, f"{anomaly:+.1f}", 1)
            pdf.cell(40, 10, risk, 1)
            pdf.ln()
            
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 10, "Note: Anomalies are calculated against a 30-year operational baseline (1991-2020). detailed climatological reports available upon request from the Department of Climate Change and Meteorological Services.")
    
    filename = "Climate_Bulletin.pdf"
    pdf.output(filename)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
