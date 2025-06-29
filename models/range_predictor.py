import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

class RangePredictor:
    """Machine learning model for predicting EV range based on various factors."""
    
    def __init__(self, model_path='models/ev_range_model.joblib'):
        self.model_path = model_path
        self.model = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Load existing model if available
        if os.path.exists(model_path):
            self.load_model()
        else:
            self.train_model()
    
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic training data based on realistic EV range factors."""
        
        np.random.seed(42)  # For reproducibility
        
        # Generate realistic ranges of values
        temperature = np.random.uniform(-10, 40, n_samples)  # Celsius
        wind_speed = np.random.uniform(0, 30, n_samples)     # km/h
        driving_styles = np.random.choice(['aggressive', 'moderate', 'eco'], n_samples)
        cargo_weight = np.random.uniform(0, 500, n_samples)  # kg
        
        # Base range (km) - typical EV range
        base_range = 400
        
        # Calculate range based on factors
        ranges = []
        for i in range(n_samples):
            range_km = base_range
            
            # Temperature effect (battery efficiency decreases in extreme temperatures)
            temp_factor = 1.0
            if temperature[i] < 0:
                temp_factor = 0.85  # Cold reduces range
            elif temperature[i] > 30:
                temp_factor = 0.90  # Heat reduces range slightly
            
            # Wind resistance effect
            wind_factor = 1.0 - (wind_speed[i] * 0.01)  # Wind reduces range
            
            # Driving style effect
            style_factor = 1.0
            if driving_styles[i] == 'aggressive':
                style_factor = 0.75  # Aggressive driving reduces range
            elif driving_styles[i] == 'eco':
                style_factor = 1.15  # Eco driving increases range
            
            # Cargo weight effect
            weight_factor = 1.0 - (cargo_weight[i] * 0.0002)  # Weight reduces range
            
            # Apply all factors
            range_km = range_km * temp_factor * wind_factor * style_factor * weight_factor
            
            # Add some realistic noise
            range_km += np.random.normal(0, 10)
            
            # Ensure range is positive and reasonable
            range_km = max(200, min(500, range_km))
            
            ranges.append(range_km)
        
        # Create DataFrame
        data = pd.DataFrame({
            'temperature': temperature,
            'wind_speed': wind_speed,
            'driving_style': driving_styles,
            'cargo_weight': cargo_weight,
            'range_km': ranges
        })
        
        return data
    
    def train_model(self):
        """Train the machine learning model."""
        print("Training EV range prediction model...")
        
        # Generate training data
        data = self.generate_synthetic_data(n_samples=2000)
        
        # Prepare features
        X = data[['temperature', 'wind_speed', 'driving_style', 'cargo_weight']].copy()
        y = data['range_km']
        
        # Encode driving style
        X['driving_style_encoded'] = self.label_encoder.fit_transform(X['driving_style'])
        X = X.drop('driving_style', axis=1)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Model training completed!")
        print(f"Training R² score: {train_score:.3f}")
        print(f"Testing R² score: {test_score:.3f}")
        
        # Save model
        self.save_model()
        self.is_trained = True
    
    def predict_range(self, temperature, wind_speed, driving_style, cargo_weight):
        """Predict EV range based on input parameters."""
        
        if not self.is_trained and self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Validate inputs
        if driving_style not in ['aggressive', 'moderate', 'eco']:
            raise ValueError("Driving style must be one of: aggressive, moderate, eco")
        
        # Prepare input data
        input_data = pd.DataFrame({
            'temperature': [temperature],
            'wind_speed': [wind_speed],
            'driving_style': [driving_style],
            'cargo_weight': [cargo_weight]
        })
        
        # Encode driving style
        input_data['driving_style_encoded'] = self.label_encoder.transform(input_data['driving_style'])
        input_data = input_data.drop('driving_style', axis=1)
        
        # Make prediction
        predicted_range = self.model.predict(input_data)[0]
        
        return predicted_range
    
    def save_model(self):
        """Save the trained model to disk."""
        if self.model is not None:
            # Create models directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # Save model and label encoder
            model_data = {
                'model': self.model,
                'label_encoder': self.label_encoder
            }
            joblib.dump(model_data, self.model_path)
            print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model from disk."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.label_encoder = model_data['label_encoder']
            self.is_trained = True
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Training new model...")
            self.train_model()
    
    def get_feature_importance(self):
        """Get feature importance from the trained model."""
        if self.model is None:
            return None
        
        feature_names = ['temperature', 'wind_speed', 'driving_style_encoded', 'cargo_weight']
        importance = self.model.feature_importances_
        
        return dict(zip(feature_names, importance)) 