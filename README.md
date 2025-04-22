# Bridge Data Visualization

Real-time visualization dashboard for bridge sensor data using Flask and Chart.js.

## Features

- Real-time temperature, humidity, and weight monitoring
- Vibration data from dual sensors
- Interactive charts with Chart.js
- Automatic data refresh
- Responsive design

## Setup

1. Install dependencies:
```sh
pip install flask
```

2. Run the server:
```sh
python server.py
```

3. Open http://localhost:5000 in your browser

## Database Schema

The application uses SQLite with two tables:

- environmental_data (temperature, humidity, weight)
- vibration_data (vibration1, vibration2)