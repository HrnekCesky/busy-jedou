from flask import Flask, render_template, jsonify
from datetime import datetime
import requests
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder='../busy_jedou/templates', static_folder='../busy_jedou/static')

# ---- VIEWS ----
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# ---- API ROUTES ----
BASE_URL = "https://api.transitous.org/api/v1"
HEADERS = {"User-Agent": "MyTestApp/1.0"}

@app.route('/api/get/stop/<text>')
def stop(text):
    try:
        response = requests.get(f"{BASE_URL}/geocode", headers=HEADERS, params={"text": text, "mode": "BUS"})
        locations = response.json()
        locs = []
        iditem = 0
        for item in locations:
            name = item.get("name")
            aa = item.get("areas")
            lat = item.get("lat")
            lon = item.get("lon")
            ab = item.get("type")
        
            if str(ab) == "STOP" and aa:
                iditem = iditem + 1
                locs.append({"id": iditem, "location": name, "kraj": aa[1].get("name"), "lat": lat, "lon": lon, "type": ab})
        
        return jsonify(locs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get/route/<place1>/<place2>')
def route(place1, place2):
    """Route endpoint - to be completed"""
    return jsonify({"status": "not implemented", "from": place1, "to": place2})

@app.route('/health')
def health():
    """Health check endpoint for Vercel"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=False)
