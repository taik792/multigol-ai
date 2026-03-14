import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for match in data.get("response", []):

    fixture = match["fixture"]
    teams = match["teams"]
    league = match["league"]

    # prendiamo solo partite NON iniziate
    if fixture["status"]["short"] != "NS":
        continue

    matches.append({

        "home": teams["home"]["name"],
        "away": teams["away"]["name"],

        "home_id": teams["home"]["id"],
        "away_id": teams["away"]["id"],

        "league": league["name"],
        "league_id": league["id"],

        "country": league["country"],

        "date": fixture["date"]

    })

print("Partite trovate:", len(matches))

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)