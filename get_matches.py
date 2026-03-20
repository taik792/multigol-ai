import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today,
    "status": "NS"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# 🔥 SOLO CAMPIONATI TOP
TOP_LEAGUES = [39, 135, 78, 61, 140]

matches = []

for match in data.get("response", []):

    if match["league"]["id"] not in TOP_LEAGUES:
        continue

    match_data = {
        "home": match["teams"]["home"]["name"],
        "away": match["teams"]["away"]["name"],
        "home_id": match["teams"]["home"]["id"],
        "away_id": match["teams"]["away"]["id"],
        "league": match["league"]["name"],
        "league_id": match["league"]["id"],
        "country": match["league"]["country"],
        "date": match["fixture"]["date"][:10],
        "time": match["fixture"]["date"][11:16]
    }

    matches.append(match_data)

    # 🔥 LIMITE PARTITE (ANTI API)
    if len(matches) >= 30:
        break

print("Partite selezionate:", len(matches))

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)