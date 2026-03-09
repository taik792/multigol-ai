import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

url = "https://v3.football.api-sports.io/fixtures"

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

TOP_LEAGUES = [
39,140,135,78,61,136,40
]

for match in data["response"]:

    if match["fixture"]["status"]["short"] != "NS":
        continue

    league_id = match["league"]["id"]

    if league_id not in TOP_LEAGUES:
        continue

    matches.append({
        "home": match["teams"]["home"]["name"],
        "away": match["teams"]["away"]["name"],
        "home_id": match["teams"]["home"]["id"],
        "away_id": match["teams"]["away"]["id"],
        "league": match["league"]["name"],
        "league_id": league_id,
        "fixture_id": match["fixture"]["id"],
        "time": match["fixture"]["date"][11:16]
    })

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)

print("Partite salvate:",len(matches))