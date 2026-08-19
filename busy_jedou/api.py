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
    res1 = requests.get(f"https://localhost/get/stop/{place1}").json()
    pos1lat = res1[0].get("lat")
    pos1lon = res1[0].get("lon")
    pos1 = f"{pos1lat},{pos1lon}"

    res2 = requests.get(f"https://localhost/get/stop/{place2}").json()
    pos2lat = res2[0].get("lat")
    pos2lon = res2[0].get("lon")
    pos2 = f"{pos2lat},{pos2lon}"

    return f"pos1: {pos1}, pos2: {pos2}"