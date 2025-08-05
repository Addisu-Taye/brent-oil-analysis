# backend/app.py
"""
Flask Backend API for Brent Oil Price Dashboard
Serves price data, events, and change point analysis results.
"""

from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os
import json
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/dist')
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
  r"/api/*": {
    "origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
  }
})
CORS(app)  # Allow all origins during dev
app = Flask(__name__, static_folder='../frontend/build')

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'backend', 'data', 'BrentOilPrices.csv')
EVENTS_PATH = os.path.join(ROOT_DIR, 'backend', 'data', 'key_oil_events.csv')


def load_brent_prices():
    df = pd.read_csv(DATA_PATH, header=None, names=['DateRaw', 'Price'])
    df['DateRaw'] = df['DateRaw'].astype(str).str.strip().str.strip('"')
    
    def parse_date(date_str):
        try:
            if '-' in date_str and len(date_str.split('-')[-1]) == 2:
                return pd.to_datetime(date_str, format='%d-%b-%y')
            else:
                return pd.to_datetime(date_str, format='%b %d, %Y')
        except:
            return pd.NaT
    df['Date'] = df['DateRaw'].apply(parse_date)
    df = df.dropna(subset=['Date']).sort_values('Date')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df[['Date', 'Price']].to_dict(orient='records')


def load_events():
    events = pd.read_csv(EVENTS_PATH)
    events['Date'] = pd.to_datetime(events['Date']).dt.strftime('%Y-%m-%d')
    return events.to_dict(orient='records')


# --- API Endpoints ---
@app.route('/api/prices')
def get_prices():
    return jsonify(load_brent_prices())

@app.route('/api/events')
def get_events():
    return jsonify(load_events())

@app.route('/api/change_points')
def get_change_points():
    # Simulated output from Bayesian model
    return jsonify([
        {
            "date": "2020-04-21",
            "pre_mean": 21.45,
            "post_mean": 75.59,
            "impact_percent": 252.1,
            "event": "OPEC+ Production Cut Agreement",
            "description": "Unprecedented 10M bpd cut to stabilize prices after pandemic crash"
        },
        {
            "date": "2022-02-24",
            "pre_mean": 92.3,
            "post_mean": 118.9,
            "impact_percent": 28.8,
            "event": "Russia Invades Ukraine",
            "description": "Energy crisis triggered by sanctions and supply fears"
        },
        {
            "date": "2005-02-25",
            "pre_mean": 21.4,
            "post_mean": 75.6,
            "impact_percent": 253.3,
            "event": "Global Demand Surge",
            "description": "Rising demand from China and India drives structural price shift"
        }
    ])

@app.route('/api/indicators')
def get_indicators():
    prices = pd.DataFrame(load_brent_prices())
    prices['Price'] = pd.to_numeric(prices['Price'], errors='coerce')
    latest_price = prices.iloc[-1]['Price']
    volatility = prices['Price'].pct_change().std() * 100 * (252**0.5)  # Annualized
    avg_price = prices['Price'].mean()

    return jsonify({
        "latest_price": round(latest_price, 2),
        "average_price": round(avg_price, 2),
        "annualized_volatility": round(volatility, 2),
        "total_events": len(load_events()),
        "detected_change_points": 3
    })

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(f"../frontend/build/{path}"):
        return send_from_directory('../frontend/build', path)
    else:
        return send_from_directory('../frontend/build', 'index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)