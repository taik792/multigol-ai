import requests
import json
from datetime import datetime

# API football (partite)
API_KEY = "b90932e65c14be06a870fd50fcd20ddc"

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.today().strftime('%Y-%m-%d')

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if "response" not in data:
    print("Errore API:", data)
    exit()

matches = []

for game in data["response"]:

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    match = {
        "home": home,
        "away": away,
        "home_goals_avg": 1.5,
        "away_goals_avg": 1.3,
        "home_conceded": 1.1,
        "away_conceded": 1.2
    }

    matches.append(match)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches salvati:", len(matches))
