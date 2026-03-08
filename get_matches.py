import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

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

matches = []

for game in data.get("response", []):

    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    matches.append({
        "home": home,
        "away": away
    })

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite trovate:", len(matches))
