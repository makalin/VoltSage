# VoltSage: Electric Vehicle Range Predictor

**Predict your EV's range with precision using machine learning.**

VoltSage is a tool that estimates an electric vehicle’s (EV) range based on weather conditions, driving style, and cargo weight. Powered by machine learning models, it provides accurate predictions to help EV drivers plan trips confidently. Built with Python, Flask, and SQLite, VoltSage is designed for easy deployment and integration via a RESTful API.

## Features
- **Range Prediction**: Estimates EV range using real-time inputs like temperature, wind speed, driving behavior (aggressive, moderate, eco), and cargo load.
- **Machine Learning**: Utilizes scikit-learn models trained on open datasets for weather and driving patterns.
- **Web Interface**: User-friendly Flask-based web app for inputting data and viewing predictions.
- **API Access**: RESTful API for developers to integrate range predictions into other applications.
- **Data Storage**: SQLite database for storing historical predictions and user inputs.
- **Open Datasets**: Leverages publicly available weather and driving data (see [Datasets](#datasets)).

## Technologies
- **Python**: Core language for ML models and backend logic.
- **scikit-learn**: For training and deploying machine learning models.
- **Flask**: Lightweight framework for web app and API.
- **SQLite**: Database for storing prediction data.
- **HTML/CSS/JavaScript**: Simple frontend for user interaction.

## Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/techdrivex/VoltSage.git
   cd voltsage
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the SQLite database:
   ```bash
   python setup_db.py
   ```
5. Run the Flask app:
   ```bash
   python app.py
   ```
6. Open your browser to `http://localhost:5000` to access the web interface.

## Usage
1. **Web Interface**:
   - Navigate to the homepage.
   - Enter weather details (e.g., temperature, wind speed), driving style, and cargo weight.
   - Click "Predict" to view the estimated EV range.
2. **API**:
   - Endpoint: `POST /api/predict`
   - Example request:
     ```bash
     curl -X POST http://localhost:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"temperature": 20, "wind_speed": 10, "driving_style": "moderate", "cargo_weight": 100}'
     ```
   - Response:
     ```json
     {"predicted_range_km": 350}
     ```

## Datasets
VoltSage uses open datasets for training its machine learning models:

- **Weather Data**: 
  - [NOAA Global Historical Climatology Network-Daily (GHCN-Daily)](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) provides daily temperature, wind, precipitation, and other meteorological data from global weather stations, ideal for modeling weather impacts on EV range.[](https://light.princeton.edu/datasets/automated_driving_dataset/)
  - [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) offers free access to hourly historical weather data (temperature, humidity, wind speed) from 1940 onward, suitable for integrating real-time weather effects.[](https://www.nature.com/articles/s41597-025-04874-4)

- **Driving Data**:
  - [DBNet Driving Behavior Dataset](http://dbnet.aitrans.online/) includes 1000 km of real-world driving data with aligned video, LiDAR point clouds, GPS, and driver behavior (speed, steering), capturing diverse driving styles for EV range prediction.[](https://medium.com/analytics-vidhya/datasets-for-machine-learning-in-autonomous-vehicles-dd13bae5925b)
  - [Canadian Adverse Driving Conditions (CADC) Dataset](https://cadcd.uwaterloo.ca/) provides 7,000 frames of winter driving data with LiDAR, camera, and GPS, focusing on adverse weather like snow, useful for modeling aggressive or eco-driving in harsh conditions.[](http://cadcd.uwaterloo.ca/)

- **Electric Vehicle Data**:
  - [UrbanEV Dataset](https://www.nature.com/articles/s41597-025-03136-7) contains six months of EV charging data from over 20,000 stations in Shenzhen, China, including weather conditions and charging patterns, relevant for correlating energy consumption with driving behavior.[](https://www.nature.com/articles/s41597-025-04874-4)
  - [Palo Alto Electric Vehicle Charging Dataset](https://data.paloalto.ca.us/datastreams/97212/electric-vehicle-charging-station-usage-july-2011-dec-2020/) offers charging session data (energy consumed, duration) from 105 stations, useful for modeling EV energy usage patterns.[](https://www.sciencedirect.com/science/article/abs/pii/S0306261924001843)

Contributions to enhance dataset integration or add new sources are welcome!

## Contributing
We welcome contributions! To get started:
1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to your fork: `git push origin feature/your-feature`.
5. Open a pull request.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and check the [Issues](https://github.com/your-username/voltsage/issues) for tasks.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

🚗 **Plan your EV journey with VoltSage!** 🌩️
