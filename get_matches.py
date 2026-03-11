import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

matches = []

for m in data["response"]:

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]
    league = m["league"]["name"]

    # ORARIO PARTITA
    utc_time = m["fixture"]["date"]

    dt = datetime.fromisoformat(utc_time.replace("Z", ""))
    dt = dt + timedelta(hours=1)

    time = dt.strftime("%H:%M")

    match = {
        "home": home,
        "away": away,
        "league": league,
        "time": time
    }

    matches.append(match)

# massimo 30 partite
matches = matches[:30]

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))
