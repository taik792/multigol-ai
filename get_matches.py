import requests
import json
import os
from datetime import datetime

# DATA DI OGGI
today = datetime.today().strftime('%Y-%m-%d')

url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={today}"

headers = {
    "X-RapidAPI-Key": "INSERISCI_LA_TUA_API_KEY",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

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

os.makedirs("data", exist_ok=True)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite aggiornate")
