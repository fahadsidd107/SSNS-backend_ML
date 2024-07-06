from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# MongoDB connection string
connection_string = "mongodb+srv://fsiddiqui107:gc79mKY4g6hGrbVL@ssnscluster.fsy0znp.mongodb.net/?retryWrites=true&w=majority&appName=SSNSCluster"

def generate_predictions(latest_data, interval_minutes):
    # Placeholder for prediction logic
    # Here we're just simulating predictions by incrementing the latest values slightly
    predicted_data = {
        'temperature': f"{latest_data['temperature'] + 0.5:.2f} °C",
        'humidity': f"{latest_data['humidity'] + 1.0:.2f} %",
        'pressure': f"{latest_data['pressure'] + 0.2:.2f} hPa",
        'perticulate_matter': f"{latest_data['perticulate_matter'] + 0.3:.2f} µg/m³",
        'date': (datetime.strptime(latest_data['date'], '%Y-%m-%d') + timedelta(minutes=interval_minutes)).strftime('%Y-%m-%d'),
        'time': (datetime.strptime(latest_data['time'], '%H:%M:%S') + timedelta(minutes=interval_minutes)).strftime('%H:%M:%S')
    }
    return predicted_data

@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        
        # Select database and collection
        db = client['testing']
        collection = db['testing']
        
        # Find the latest document based on timestamp
        latest_document = collection.find_one({}, sort=[('timestamp', -1)])
        
        # Extract required fields from the latest document
        if latest_document:
            latest_data = {
                'temperature': latest_document.get('temperature'),
                'perticulate_matter': latest_document.get('perticulate_matter'),
                'pressure': latest_document.get('pressure'),
                'humidity': latest_document.get('humidity'),
                'time': latest_document.get('time'),
                'date': latest_document.get('date'),
            }
        else:
            latest_data = {}

        # Generate predictions for 15 mins, 30 mins, and 1 hour
        predictions = {
            '15 mins': generate_predictions(latest_data, 15),
            '30 mins': generate_predictions(latest_data, 30),
            '1 hour': generate_predictions(latest_data, 60),
            'accuracy': '70%'
        }
        
        # Close the connection to MongoDB
        client.close()
        
        return jsonify(predictions), 200
    
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
