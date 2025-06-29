from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime
from models.range_predictor import RangePredictor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize the range predictor
predictor = RangePredictor()

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('voltsage.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main page with the range prediction form."""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_range():
    """API endpoint for range prediction."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['temperature', 'wind_speed', 'driving_style', 'cargo_weight']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract parameters
        temperature = float(data['temperature'])
        wind_speed = float(data['wind_speed'])
        driving_style = data['driving_style']
        cargo_weight = float(data['cargo_weight'])
        
        # Validate driving style
        valid_styles = ['aggressive', 'moderate', 'eco']
        if driving_style not in valid_styles:
            return jsonify({'error': 'Invalid driving style. Must be one of: aggressive, moderate, eco'}), 400
        
        # Make prediction
        predicted_range = predictor.predict_range(
            temperature=temperature,
            wind_speed=wind_speed,
            driving_style=driving_style,
            cargo_weight=cargo_weight
        )
        
        # Store prediction in database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO predictions (temperature, wind_speed, driving_style, cargo_weight, predicted_range, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (temperature, wind_speed, driving_style, cargo_weight, predicted_range, datetime.now()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'predicted_range_km': round(predicted_range, 2),
            'temperature': temperature,
            'wind_speed': wind_speed,
            'driving_style': driving_style,
            'cargo_weight': cargo_weight
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid numeric values provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """API endpoint to get prediction history."""
    try:
        conn = get_db_connection()
        predictions = conn.execute('''
            SELECT * FROM predictions 
            ORDER BY created_at DESC 
            LIMIT 50
        ''').fetchall()
        conn.close()
        
        history = []
        for pred in predictions:
            history.append({
                'id': pred['id'],
                'temperature': pred['temperature'],
                'wind_speed': pred['wind_speed'],
                'driving_style': pred['driving_style'],
                'cargo_weight': pred['cargo_weight'],
                'predicted_range': pred['predicted_range'],
                'created_at': pred['created_at']
            })
        
        return jsonify(history)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history_page():
    """Page to display prediction history."""
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 