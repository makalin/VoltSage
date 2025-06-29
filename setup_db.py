import sqlite3
import os

def setup_database():
    """Create the SQLite database and tables."""
    
    # Remove existing database if it exists
    if os.path.exists('voltsage.db'):
        os.remove('voltsage.db')
        print("Removed existing database.")
    
    # Create new database
    conn = sqlite3.connect('voltsage.db')
    cursor = conn.cursor()
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL NOT NULL,
            wind_speed REAL NOT NULL,
            driving_style TEXT NOT NULL,
            cargo_weight REAL NOT NULL,
            predicted_range REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX idx_created_at ON predictions(created_at)
    ''')
    
    # Insert some sample data for testing
    sample_data = [
        (20.0, 10.0, 'moderate', 100.0, 350.0),
        (25.0, 5.0, 'eco', 50.0, 380.0),
        (15.0, 15.0, 'aggressive', 200.0, 320.0),
        (30.0, 8.0, 'moderate', 150.0, 340.0),
        (10.0, 20.0, 'eco', 75.0, 360.0)
    ]
    
    cursor.executemany('''
        INSERT INTO predictions (temperature, wind_speed, driving_style, cargo_weight, predicted_range)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_data)
    
    conn.commit()
    conn.close()
    
    print("Database setup completed successfully!")
    print("Created 'voltsage.db' with predictions table and sample data.")

if __name__ == '__main__':
    setup_database() 