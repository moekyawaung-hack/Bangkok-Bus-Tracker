import json

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_bus_routes():
    return load_json("data/bus_routes.json")

def load_stops():
    return load_json("data/stops.json")
