import requests
import json
from datetime import datetime
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.now().strftime("%Y-%m-%d")

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for m in data["response"]:
    try:
        match = {
            "fixture_id": m["fixture"]["id"],
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "date": m["fixture"]["date"],
            "league": m["league"]["name"],
            "country": m["league"]["country"]
        }
        matches.append(match)
    except:
        continue

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"Scaricate {len(matches)} partite di oggi")