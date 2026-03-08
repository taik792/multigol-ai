import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.today().strftime('%Y-%m-%d')

params = {
    "date": today,
    "status": "NS"
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

matches = []

for game in data["response"]:

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]
    date_match = game["fixture"]["date"]
    league = game["league"]["name"]

    matches.append({
        "home": home,
        "away": away,
        "date": date_match,
        "league": league
    })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches trovate:", len(matches))
