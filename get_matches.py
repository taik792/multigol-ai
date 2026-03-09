import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for match in data["response"]:

    if match["fixture"]["status"]["short"] != "NS":
        continue

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_id = match["teams"]["home"]["id"]
    away_id = match["teams"]["away"]["id"]

    league = match["league"]["name"]
    league_id = match["league"]["id"]

    time = match["fixture"]["date"][11:16]

    matches.append({
        "home": home,
        "away": away,
        "home_id": home_id,
        "away_id": away_id,
        "league": league,
        "league_id": league_id,
        "time": time
    })

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))