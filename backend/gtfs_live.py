import requests
from config.settings import GTFS_REALTIME_URL

def fetch_live_positions():
    try:
        r = requests.get(GTFS_REALTIME_URL, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return {"error": "offline"}
