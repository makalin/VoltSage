#!/usr/bin/env python3
"""
VoltSage Startup Script
Run this script to start the VoltSage EV Range Predictor application.
"""

import os
import sys
from app import app
from config import config

def main():
    """Main function to start the VoltSage application."""
    
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Apply configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Print startup information
    print("🚗 VoltSage EV Range Predictor")
    print("=" * 50)
    print(f"Environment: {config_name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Database: {app.config['DATABASE_PATH']}")
    print(f"Model path: {app.config['MODEL_PATH']}")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists(app.config['DATABASE_PATH']):
        print("⚠️ Database not found. Please run setup_db.py first.")
        print("   python setup_db.py")
        sys.exit(1)
    
    # Start the application
    try:
        print(f"🌐 Starting server on http://{app.config['HOST']}:{app.config['PORT']}")
        print("📱 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG']
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 