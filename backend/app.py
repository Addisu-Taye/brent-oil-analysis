# backend/app.py
"""
Flask Backend API for Brent Oil Price Dashboard
Serves cleaned data, events, and model results to React frontend.
"""

from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os
import csv

app = Flask(__name__, static_folder='../frontend/dist')

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'data', 'BrentOilPrices_clean.csv')
EVENTS_PATH = os.path.join(ROOT_DIR, 'events', 'key_oil_events.csv')
ANALYSIS_2005_PATH = os.path.join(ROOT_DIR, 'analysis_summary.csv')
ANALYSIS_2020_PATH = os.path.join(ROOT_DIR, 'analysis_summary_2020.csv')


def load_brent_prices():
    """Fix and load Brent oil prices with mixed date formats."""
    if not os.path.exists(DATA_PATH):
        with open(os.path.join(ROOT_DIR, 'BrentOilPrices.csv'), 'r') as f:
            content = f.read().replace('\n', '').replace('\r', '')
        import re
        pattern = r'(?:\"([A-Za-z]{3} \d{1,2}, \d{4})\"|(\d{1,2}-[A-Za-z]{3}-\d{2})),([0-9]+\.[0-9]+)'
        matches = re.findall(pattern, content)
        records = [{'Date': m[0] if m[0] else m[1], 'Price': float(m[2])} for m in matches]
        df = pd.DataFrame(records)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
    return df[['Date', 'Price']].to_dict(orient='records')


def load_events():
    """Load key events from CSV."""
    if not os.path.exists(EVENTS_PATH):
        # Create default events
        events = [
            ("Iraq Invades Kuwait", "1990-08-02", "Triggers Gulf War; prices spike from $20 to $46"),
            ("OPEC+ Agreement", "2020-04-12", "Unprecedented 10M bpd cut to stabilize prices"),
            ("Russia Invades Ukraine", "2022-02-24", "Triggers energy crisis and sanctions"),
            ("US-China Trade War", "2018-03-08", "Tariffs raise concerns over global demand"),
            ("Global Financial Crisis", "2008-09-15", "Lehman collapse leads to demand crash"),
        ]
        df = pd.DataFrame(events, columns=['Event', 'Date', 'Description'])
        df.to_csv(EVENTS_PATH, index=False)
    df = pd.read_csv(EVENTS_PATH)
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')


def load_analysis_summary(file_path):
    """Load analysis summary safely."""
    try:
        with open(file_path, mode='r') as f:
            reader = csv.DictReader(f)
            return next(reader)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}


# --- API Endpoints ---
@app.route('/api/prices')
def get_prices():
    return jsonify(load_brent_prices())

@app.route('/api/events')
def get_events():
    return jsonify(load_events())

@app.route('/api/change_points')
def get_change_points():
    summary_2005 = load_analysis_summary(ANALYSIS_2005_PATH)
    summary_2020 = load_analysis_summary(ANALYSIS_2020_PATH)
    return jsonify([
        {
            "date": summary_2005.get("Change Point Date", "").split()[0],
            "pre_mean": float(summary_2005.get("Pre-Change Mean", 0)),
            "post_mean": float(summary_2005.get("Post-Change Mean", 0)),
            "impact_percent": round(
                (float(summary_2005.get("Post-Change Mean", 0)) - float(summary_2005.get("Pre-Change Mean", 0)))
                / float(summary_2005.get("Pre-Change Mean", 1)) * 100, 1),
            "event": "Global Demand Surge (2005)",
            "description": "Rising demand from China and India drives structural price shift"
        },
        {
            "date": summary_2020.get("Change Point Date", "").split()[0],
            "pre_mean": float(summary_2020.get("Pre-Change Mean", 0)),
            "post_mean": float(summary_2020.get("Post-Change Mean", 0)),
            "impact_percent": round(
                (float(summary_2020.get("Post-Change Mean", 0)) - float(summary_2020.get("Pre-Change Mean", 0)))
                / float(summary_2020.get("Pre-Change Mean", 1)) * 100, 1),
            "event": "OPEC+ Production Cut (2020)",
            "description": "Historic 10M bpd cut stabilizes prices after pandemic crash"
        }
    ])

@app.route('/api/indicators')
def get_indicators():
    prices = pd.DataFrame(load_brent_prices())
    prices['Price'] = pd.to_numeric(prices['Price'], errors='coerce')
    latest_price = prices.iloc[-1]['Price']
    avg_price = prices['Price'].mean()
    volatility = prices['Price'].pct_change().std() * 100 * (252**0.5)
    return jsonify({
        "latest_price": round(latest_price, 2),
        "average_price": round(avg_price, 2),
        "annualized_volatility": round(volatility, 2),
        "total_events": len(load_events()),
        "detected_change_points": 2
    })

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(f"../frontend/dist/{path}"):
        return send_from_directory('../frontend/dist', path)
    else:
        return send_from_directory('../frontend/dist', 'index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)