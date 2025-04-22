from flask import Flask, request, render_template, jsonify
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# SQLite Database setup
def init_db():
    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS environmental_data (
            id INTEGER PRIMARY KEY,
            temperature REAL,
            humidity REAL,
            weight REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vibration_data (
            id INTEGER PRIMARY KEY,
            vibration1 REAL,
            vibration2 REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Endpoint to receive environmental data
@app.route('/upload_environmental_data', methods=['POST'])
def upload_environmental_data():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    weight = data.get('weight')

    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO environmental_data (temperature, humidity, weight)
        VALUES (?, ?, ?)
    ''', (temperature, humidity, weight))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200

# Endpoint to receive vibration data
@app.route('/upload_vibration_data', methods=['POST'])
def upload_vibration_data():
    data = request.json
    vibration1 = data.get('vibration1')
    vibration2 = data.get('vibration2')

    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vibration_data (vibration1, vibration2)
        VALUES (?, ?)
    ''', (vibration1, vibration2))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200

# Fetch data for plotting
@app.route('/')
def index():
    return render_template('index.html')

# Get temperature, humidity, and weight data for plotting
@app.route('/get_environmental_data')
def get_environmental_data():
    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT temperature, humidity, weight, timestamp FROM environmental_data ORDER BY timestamp DESC LIMIT 100')
    rows = cursor.fetchall()

    conn.close()

    timestamps, temperatures, humidities, weights = [], [], [], []

    for row in rows:
        timestamps.append(row[3])
        temperatures.append(row[0])
        humidities.append(row[1])
        weights.append(row[2])

    return jsonify({
        'timestamps': timestamps,
        'temperatures': temperatures,
        'humidities': humidities,
        'weights': weights
    })

# Get vibration data for plotting
@app.route('/get_vibration_data')
def get_vibration_data():
    conn = sqlite3.connect('sensors_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT vibration1, vibration2, timestamp FROM vibration_data ORDER BY timestamp DESC LIMIT 100')
    rows = cursor.fetchall()

    conn.close()

    timestamps, vibration1s, vibration2s = [], [], []

    for row in rows:
        timestamps.append(row[2])
        vibration1s.append(row[0])
        vibration2s.append(row[1])

    return jsonify({
        'timestamps': timestamps,
        'vibration1s': vibration1s,
        'vibration2s': vibration2s
    })

# Run the Flask server
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
