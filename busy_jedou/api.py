from busy_jedou import app
import requests

STOP_LOOKUP_BASE_URL = "https://api.transitous.org/api/v1"
ROUTE_LOOKUP_BASE_URL = "https://api.transitous.org/api/v6"
HEADERS={"User-Agent": "MyTestApp/1.0"}

@app.route('/get/stop/<text>')
def stop(text):
    response = requests.get(f"{STOP_LOOKUP_BASE_URL}/geocode", headers=HEADERS, params={"text": text, "mode": "BUS"})

    locations = response.json()
    locs = []
    iditem = 0
    for item in locations:
        name = item.get("name")
        aa = item.get("areas")
        lat = item.get("lat")
        lon = item.get("lon")
        stop_id = item.get("id")
        ab = item.get("type")
    
        if str(ab) == "STOP":
            iditem = iditem + 1
            kraj = aa[1].get("name")
            locs.append({"id": iditem, "location": name, "kraj": kraj, "lat": lat, "lon": lon, "stop_id": stop_id, "type": ab})
    
    return locs

@app.route('/get/route/search/<place1>/<num1>/<place2>/<num2>')
def route(place1, place2, num1, num2):
    num1 = int(num1)
    num2 = int(num2)

    res1 = stop(place1)
    name1 = res1[num1].get("location") + ", " + res1[num1].get("kraj")
    pos1lat = res1[num1].get("lat")
    pos1lon = res1[num1].get("lon")
    id1 = res1[num1].get("stop_id")
    pos1 = {"name": name1, "lat": pos1lat, "lon": pos1lon, "stop_id": id1}

    res2 = stop(place2)
    name2 = res2[num2].get("location") + ", " + res2[num2].get("kraj")
    pos2lat = res2[num2].get("lat")
    pos2lon = res2[num2].get("lon")
    id2 = res2[num2].get("stop_id")
    pos2 = {"name": name2, "lat": pos2lat, "lon": pos2lon, "stop_id": id2}

    response = requests.get(f"{ROUTE_LOOKUP_BASE_URL}/plan", headers=HEADERS, params={"fromPlace": id1, "toPlace": id2, "transitModes": "BUS"})
    return {"places": {"departure": pos1, "destination": pos2}, "routing": response.json()}