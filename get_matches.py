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
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for m in data["response"]:

    if m["fixture"]["status"]["short"] != "NS":
        continue

    match = {
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "league": m["league"]["name"],
        "country": m["league"]["country"],
        "date": m["fixture"]["date"]
    }

    matches.append(match)

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))