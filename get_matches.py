import requests
import json
import os
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

today = datetime.today().strftime('%Y-%m-%d')

url = f"https://v3.football.api-sports.io/fixtures?date={today}"

headers = {
    "x-apisports-key": API_KEY,
    "x-apisports-host": "v3.football.api-sports.io"
}

response = requests.get(url, headers=headers)
data = response.json()

matches = []

if "response" in data:

    for game in data["response"]:

        home = game["teams"]["home"]["name"]
        away = game["teams"]["away"]["name"]
        league = game["league"]["name"]

        matches.append({
            "home": home,
            "away": away,
            "league": league,
            "home_goals_avg": 1.5,
            "away_goals_avg": 1.3,
            "home_conceded": 1.1,
            "away_conceded": 1.2
        })

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches aggiornati")
