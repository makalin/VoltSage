# VoltSage Quick Start Guide

Get VoltSage up and running in minutes! 🚗⚡

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/makalin/VoltSage.git
cd VoltSage
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Database

```bash
python setup_db.py
```

### 5. Start the Application

```bash
python run.py
```

The application will be available at: **http://localhost:5000**

## Quick Test

### Test the Machine Learning Model

```bash
python test_app.py
```

This will test the core functionality without needing the web server.

### Test the Web Interface

1. Open your browser to `http://localhost:5000`
2. Fill out the prediction form:
   - Temperature: 20°C
   - Wind Speed: 10 km/h
   - Driving Style: Moderate
   - Cargo Weight: 100 kg
3. Click "Predict Range"
4. View your predicted EV range!

### Test the API

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 20,
    "wind_speed": 10,
    "driving_style": "moderate",
    "cargo_weight": 100
  }'
```

## Project Structure

```
VoltSage/
├── app.py                 # Main Flask application
├── run.py                 # Startup script
├── setup_db.py           # Database initialization
├── test_app.py           # Test suite
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── models/
│   ├── __init__.py
│   └── range_predictor.py # ML model for predictions
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main prediction page
│   └── history.html      # Prediction history page
└── docs/
    └── API.md            # API documentation
```

## Features

- ✅ **Range Prediction**: Predict EV range based on weather and driving conditions
- ✅ **Web Interface**: User-friendly form for inputting parameters
- ✅ **REST API**: Programmatic access to predictions
- ✅ **History Tracking**: View past predictions and statistics
- ✅ **Machine Learning**: Advanced ML model for accurate predictions
- ✅ **Responsive Design**: Works on desktop and mobile devices

## Configuration

Copy the environment example file and customize as needed:

```bash
cp env.example .env
# Edit .env with your settings
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in .env file or use different port
   python run.py --port 5001
   ```

2. **Database errors**
   ```bash
   # Recreate database
   python setup_db.py
   ```

3. **Import errors**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Model training issues**
   ```bash
   # Check available memory and disk space
   # The model requires ~100MB for training
   ```

### Getting Help

- Check the logs in the console output
- Review the API documentation in `docs/API.md`
- Run the test suite: `python test_app.py`

## Next Steps

1. **Customize the Model**: Modify `models/range_predictor.py` to use real EV data
2. **Add Weather Integration**: Connect to real weather APIs
3. **Deploy to Production**: Use WSGI server like Gunicorn
4. **Add Authentication**: Implement API keys or user accounts
5. **Mobile App**: Build a mobile app using the REST API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy EV planning!** 🌱⚡🚗 