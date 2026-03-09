import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# campionati TOP + serie inferiori
TOP_LEAGUES = [
39,40,       # Premier League + Championship
140,141,     # La Liga + La Liga 2
135,136,     # Serie A + Serie B
78,79,       # Bundesliga + Bundesliga 2
61,62,       # Ligue 1 + Ligue 2
2,3,848,     # Champions League / Europa / Conference
]

matches = []

for match in data["response"]:

    league_id = match["league"]["id"]

    if league_id not in TOP_LEAGUES:
        continue

    status = match["fixture"]["status"]["short"]

    if status != "NS":
        continue

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    league = match["league"]["name"]

    time = match["fixture"]["date"][11:16]

    matches.append({
        "home": home,
        "away": away,
        "league": league,
        "time": time
    })

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=4)

print("Partite salvate:", len(matches))
