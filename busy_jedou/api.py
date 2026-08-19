from busy_jedou import app
import requests

BASE_URL = "https://api.transitous.org/api/v1"
HEADERS={"User-Agent": "MyTestApp/1.0"}

@app.route('/get/stop/<text>')
def stop(text):
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
    
        if str(ab) == "STOP":
            iditem = iditem + 1
            kraj = aa[1].get("name") if isinstance(aa, list) and len(aa) > 1 and aa[1] else None
            locs.append({"id": iditem, "location": name, "kraj": kraj, "lat": lat, "lon": lon, "type": ab})
    
    return locs

@app.route('/get/route/<place1>/<place2>')
def route(place1, place2):
    return "a"