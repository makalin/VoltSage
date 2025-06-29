# VoltSage API Documentation

## Overview

VoltSage provides a RESTful API for predicting electric vehicle range based on various environmental and driving factors. The API is built with Flask and returns JSON responses.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth2.

## Endpoints

### 1. Predict EV Range

**POST** `/api/predict`

Predicts the range of an electric vehicle based on input parameters.

#### Request Body

```json
{
  "temperature": 20.0,
  "wind_speed": 10.0,
  "driving_style": "moderate",
  "cargo_weight": 100.0
}
```

#### Parameters

| Parameter | Type | Required | Description | Range |
|-----------|------|----------|-------------|-------|
| `temperature` | float | Yes | Temperature in Celsius | -40 to 50 |
| `wind_speed` | float | Yes | Wind speed in km/h | 0 to 100 |
| `driving_style` | string | Yes | Driving style | "eco", "moderate", "aggressive" |
| `cargo_weight` | float | Yes | Cargo weight in kg | 0 to 1000 |

#### Response

**Success (200 OK)**
```json
{
  "predicted_range_km": 350.25,
  "temperature": 20.0,
  "wind_speed": 10.0,
  "driving_style": "moderate",
  "cargo_weight": 100.0
}
```

**Error (400 Bad Request)**
```json
{
  "error": "Missing required field: temperature"
}
```

**Error (400 Bad Request)**
```json
{
  "error": "Invalid driving style. Must be one of: aggressive, moderate, eco"
}
```

#### Example Usage

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

### 2. Get Prediction History

**GET** `/api/history`

Retrieves the history of predictions made through the API.

#### Response

**Success (200 OK)**
```json
[
  {
    "id": 1,
    "temperature": 20.0,
    "wind_speed": 10.0,
    "driving_style": "moderate",
    "cargo_weight": 100.0,
    "predicted_range": 350.25,
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "temperature": 25.0,
    "wind_speed": 5.0,
    "driving_style": "eco",
    "cargo_weight": 50.0,
    "predicted_range": 380.75,
    "created_at": "2024-01-15T11:15:00"
  }
]
```

#### Example Usage

```bash
curl -X GET http://localhost:5000/api/history
```

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Request successful
- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: Server error

All error responses include an `error` field with a descriptive message.

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing rate limiting to prevent abuse.

## Data Storage

All predictions are stored in a SQLite database (`voltsage.db`) with the following schema:

```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    wind_speed REAL NOT NULL,
    driving_style TEXT NOT NULL,
    cargo_weight REAL NOT NULL,
    predicted_range REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Machine Learning Model

The range prediction is powered by a Random Forest model trained on synthetic data that considers:

- **Temperature effects**: Battery efficiency decreases in extreme temperatures
- **Wind resistance**: Higher wind speeds reduce range
- **Driving style**: Aggressive driving reduces range, eco driving increases it
- **Cargo weight**: Heavier loads reduce range

The model is automatically trained when the application starts and saved to `models/ev_range_model.joblib`.

## Future Enhancements

Planned API improvements:

1. **Authentication**: API key or OAuth2 implementation
2. **Rate limiting**: Request throttling
3. **Real-time weather**: Integration with weather APIs
4. **Vehicle profiles**: Support for different EV models
5. **Batch predictions**: Multiple predictions in one request
6. **Prediction confidence**: Confidence intervals for predictions 