import requests
import json
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

# 📅 oggi + domani
today = datetime.utcnow().strftime("%Y-%m-%d")
tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")

matches = []

for date in [today, tomorrow]:

    params = {
        "date": date,
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "response" in data:
        for match in data["response"]:
            try:
                fixture = match["fixture"]
                teams = match["teams"]
                league = match["league"]

                match_data = {
                    "fixture_id": fixture["id"],
                    "date": fixture["date"][:10],
                    "time": fixture["date"][11:16],
                    "home": teams["home"]["name"],
                    "away": teams["away"]["name"],
                    "home_id": teams["home"]["id"],
                    "away_id": teams["away"]["id"],
                    "league": league["name"],
                    "country": league["country"]
                }

                matches.append(match_data)

            except:
                continue

# 📁 salva file
os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=2)

print("Partite trovate:", len(matches))