import requests
import json
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

now = datetime.utcnow() + timedelta(hours=2)
today = now.strftime("%Y-%m-%d")

print("DATA USATA:", today)

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# 🧹 pulizia
if os.path.exists("data/matches_today.json"):
    os.remove("data/matches_today.json")

matches = []

for m in data["response"]:

    # 🔥 SOLO NON INIZIATE
    if m["fixture"]["status"]["short"] != "NS":
        continue

    match = {
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "date": m["fixture"]["date"],
        "league": m["league"]["name"],
        "country": m["league"]["country"]
    }

    matches.append(match)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"Scaricate {len(matches)} partite NUOVE")