# Malawi Climate Monitor

A professional, Python-based climate analytics application built with **Flask** and **Tailwind CSS**.
Designed to monitor real-time weather conditions across major Malawian cities with a premium, glassmorphism UI.

![Dashboard Preview](Images/Weather%20App%20Preview.png)

## Features

- **Climate Diagnostics**: Real-time anomaly detection against a 30-year operational baseline (1991-2020).
- **Heat Stress Index**: Automated risk assessment (Safe, Caution, Danger) based on temperature and humidity.
- **Geospatial Intelligence**: Interactive Leaflet map showing the live status of the station network.
- **Policy Reporting**: One-click generation of the "National Climate Bulletin" (PDF) for stakeholders.
- **Live Weather Data**: Real-time integration with OpenWeatherMap API.
- **5-Day Forecast**: Predictive analytics for upcoming weather patterns.
- **Dynamic Aesthetics**: Background visuals adapt automatically to current weather conditions.
- **Multi-Station Monitoring**: Lilongwe, Blantyre, Mzuzu, Zomba.

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, Jinja2 Templates, Tailwind CSS
- **Geospatial**: Folium (Leaflet.js)
- **Reporting**: FPDF (Automated PDF Generation)
- **Visualization**: Chart.js
- **API**: OpenWeatherMap

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/Jimmy-JayJay/malawi-climate-monitor.git
    cd malawi-climate-monitor
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**

    ```bash
    python app.py
    ```

4.  **Access the Dashboard**
    Open your browser and navigate to `http://127.0.0.1:5000`

## Future Roadmap

-  Database integration (SQLite/PostgreSQL) for long-term historical data.
-  Email alerts for extreme weather events.


---

_Built by [Jimmy Edward Matewere](https://www.linkedin.com/in/jimmy-matewere) - Climate Scientist & Data Analyst._
