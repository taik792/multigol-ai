import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

r = requests.get(url, headers=headers, params=params)
data = r.json()

matches = []

for m in data.get("response", []):

    matches.append({
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "league": m["league"]["name"],
        "season": m["league"]["season"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "league_id": m["league"]["id"]
    })

with open("data/matches_today.json","w") as f:
    json.dump(matches[:20],f,indent=4)

print("matches:",len(matches))
