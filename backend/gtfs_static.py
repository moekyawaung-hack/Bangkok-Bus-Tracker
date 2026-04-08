import csv
import os
from config.settings import GTFS_STATIC_PATH

def load_gtfs_table(name):
    path = os.path.join(GTFS_STATIC_PATH, f"{name}.txt")
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def build_route_index():
    routes = load_gtfs_table("routes")
    trips = load_gtfs_table("trips")
    stop_times = load_gtfs_table("stop_times")
    stops = load_gtfs_table("stops")

    routes_by_id = {r["route_id"]: r for r in routes}
    trips_by_route = {}
    for t in trips:
        trips_by_route.setdefault(t["route_id"], []).append(t["trip_id"])

    stops_by_trip = {}
    for st in stop_times:
        stops_by_trip.setdefault(st["trip_id"], []).append(st["stop_id"])

    stops_by_id = {s["stop_id"]: s for s in stops}

    route_index = {}
    for route_id, trip_ids in trips_by_route.items():
        route = routes_by_id[route_id]
        sample_trip = trip_ids[0]
        stop_ids = stops_by_trip.get(sample_trip, [])
        stop_names = [stops_by_id[s]["stop_name"] for s in stop_ids if s in stops_by_id]
        route_index[route["route_short_name"]] = {
            "name": route["route_long_name"],
            "stops": stop_names
        }
    return route_index
