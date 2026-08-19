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
            kraj = aa[1].get("name")
            locs.append({"id": iditem, "location": name, "kraj": kraj, "lat": lat, "lon": lon, "type": ab})
    
    return locs

@app.route('/get/route/search/<place1>/<num1>/<place2>/<num2>')
def route(place1, place2, num1, num2):
    res1 = stop(place1)
    name1 = res1[num1].get("location") + ", " + res1[num1].get("kraj")
    pos1lat = res1[num1].get("lat")
    pos1lon = res1[num1].get("lon")
    pos1 = f"{name1}: {pos1lat}, {pos1lon} <br />"

    res2 = stop(place2)
    name2 = res2[num2].get("location") + ", " + res2[num2].get("kraj")
    pos2lat = res2[num2].get("lat")
    pos2lon = res2[num2].get("lon")
    pos2 = f"{name2}: {pos2lat}, {pos2lon} <br />"

    return f"pos1: {pos1} pos2: {pos2}"