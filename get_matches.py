import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures?date=" + datetime.now().strftime("%Y-%m-%d")

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []

for m in data["response"]:
    matches.append({
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "league_id": m["league"]["id"],
        "season": m["league"]["season"],
        "date": m["fixture"]["date"],
        "league": m["league"]["name"],
        "country": m["league"]["country"]
    })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"Scaricate {len(matches)} partite")