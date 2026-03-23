import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.utcnow().strftime("%Y-%m-%d")

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "date": today
}

res = requests.get(url, headers=headers, params=params)
data = res.json()

matches = []

for m in data.get("response", []):
    fixture = m["fixture"]
    teams = m["teams"]

    matches.append({
        "fixture_id": fixture["id"],
        "home": teams["home"]["name"],
        "away": teams["away"]["name"],
        "date": fixture["date"]
    })

# salva SOLO matches_today
with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"✅ Matches salvate: {len(matches)}")