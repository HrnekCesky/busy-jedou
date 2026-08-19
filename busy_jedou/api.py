from busy_jedou import app
import requests
import datetime
from flask import request

STOP_LOOKUP_BASE_URL = "https://api.transitous.org/api/v1"
ROUTE_LOOKUP_BASE_URL = "https://api.transitous.org/api/v6"
HEADERS={"User-Agent": "MyTestApp/1.0"}

@app.route('/get/stop/<text>', methods=['GET'])
def get_stop(text):
    return stop(text)

@app.route('/get/route/<place1>/<num1>/<place2>/<num2>', methods=['GET'])
def get_route(place1, place2, num1, num2):
    return route(place1, place2, num1, num2)

@app.route('/get/stop/', methods=['POST'])
def stop():
    text = request.args("text")

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

@app.route('/get/route/', methods=['POST'])
def route():
    place1 = request.args("place1")
    place2 = request.args("place2")
    num1 = request.args("num1")
    num2 = request.args("num2")

    num1 = int(num1)
    num2 = int(num2)
    place1 = str(place1)
    place2 = str(place2)

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

    route = requests.get(f"{ROUTE_LOOKUP_BASE_URL}/plan", headers=HEADERS, params={"fromPlace": id1, "toPlace": id2, "transitModes": "BUS"})
    routejson = route.json()

    busy = routejson["itineraries"]
        
    out = []
    for i in range(len(busy)):
        busya = busy[i].get("legs")

        busy_from = busya[0].get("from")
        busy_from_name = busy_from.get("name")
        busy_from_scheduledDeparture = busy_from.get("scheduledDeparture")
        busy_from_scheduledDeparture = datetime.datetime.fromisoformat(busy_from_scheduledDeparture.replace("Z", "+00:00"))
        busy_from_scheduledDeparture = busy_from_scheduledDeparture.astimezone(datetime.timezone(datetime.timedelta(hours=2))).isoformat()

        busy_to = busya[0].get("to")
        busy_to_name = busy_to.get("name")
        busy_to_scheduledArrival = busy_to.get("scheduledArrival")
        busy_to_scheduledArrival = datetime.datetime.fromisoformat(busy_to_scheduledArrival.replace("Z", "+00:00"))
        busy_to_scheduledArrival = busy_to_scheduledArrival.astimezone(datetime.timezone(datetime.timedelta(hours=2))).isoformat()

        out.append({"id": i, "data": {"from": {"name": busy_from_name, "scheduledDeparture": busy_from_scheduledDeparture}, "to": {"name": busy_to_name, "scheduledArrival": busy_to_scheduledArrival}}})
      
    return out