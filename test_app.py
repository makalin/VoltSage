#!/usr/bin/env python3
"""
Test script for VoltSage EV Range Predictor
"""

import requests
import json
import time
from models.range_predictor import RangePredictor

def test_model():
    """Test the machine learning model."""
    print("🧪 Testing Machine Learning Model...")
    
    try:
        # Initialize predictor
        predictor = RangePredictor()
        
        # Test predictions
        test_cases = [
            {
                'temperature': 20,
                'wind_speed': 10,
                'driving_style': 'moderate',
                'cargo_weight': 100,
                'description': 'Normal conditions'
            },
            {
                'temperature': -5,
                'wind_speed': 25,
                'driving_style': 'aggressive',
                'cargo_weight': 300,
                'description': 'Harsh conditions'
            },
            {
                'temperature': 25,
                'wind_speed': 5,
                'driving_style': 'eco',
                'cargo_weight': 50,
                'description': 'Optimal conditions'
            }
        ]
        
        for case in test_cases:
            predicted_range = predictor.predict_range(
                temperature=case['temperature'],
                wind_speed=case['wind_speed'],
                driving_style=case['driving_style'],
                cargo_weight=case['cargo_weight']
            )
            
            print(f"✅ {case['description']}: {predicted_range:.1f} km")
        
        # Test feature importance
        importance = predictor.get_feature_importance()
        if importance:
            print("\n📊 Feature Importance:")
            for feature, imp in importance.items():
                print(f"   {feature}: {imp:.3f}")
        
        print("✅ Model tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_api():
    """Test the Flask API endpoints."""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_data = {
        "temperature": 20,
        "wind_speed": 10,
        "driving_style": "moderate",
        "cargo_weight": 100
    }
    
    try:
        # Test prediction endpoint
        print("Testing /api/predict...")
        response = requests.post(
            f"{base_url}/api/predict",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful: {result['predicted_range_km']} km")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(response.text)
            return False
        
        # Test history endpoint
        print("Testing /api/history...")
        response = requests.get(f"{base_url}/api/history")
        
        if response.status_code == 200:
            history = response.json()
            print(f"✅ History retrieved: {len(history)} predictions")
        else:
            print(f"❌ History failed: {response.status_code}")
            print(response.text)
            return False
        
        print("✅ API tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API test failed: Flask app not running")
        print("   Start the app with: python app.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_web_interface():
    """Test the web interface."""
    print("\n🖥️ Testing Web Interface...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test main page
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Main page accessible")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
        
        # Test history page
        response = requests.get(f"{base_url}/history")
        if response.status_code == 200:
            print("✅ History page accessible")
        else:
            print(f"❌ History page failed: {response.status_code}")
            return False
        
        print("✅ Web interface tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Web interface test failed: Flask app not running")
        return False
    except Exception as e:
        print(f"❌ Web interface test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚗 VoltSage Test Suite")
    print("=" * 50)
    
    # Test model
    model_ok = test_model()
    
    # Test API (only if Flask app is running)
    api_ok = test_api()
    
    # Test web interface (only if Flask app is running)
    web_ok = test_web_interface()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   Machine Learning Model: {'✅ PASS' if model_ok else '❌ FAIL'}")
    print(f"   API Endpoints: {'✅ PASS' if api_ok else '❌ FAIL (Flask not running)'}")
    print(f"   Web Interface: {'✅ PASS' if web_ok else '❌ FAIL (Flask not running)'}")
    
    if model_ok:
        print("\n🎉 Core functionality is working!")
        if not (api_ok and web_ok):
            print("💡 To test API and web interface, start the Flask app:")
            print("   python app.py")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 