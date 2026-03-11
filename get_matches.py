import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "date": today
}

response = requests.get(url, headers=headers, params=params).json()

matches = []

for m in response["response"]:

    match = {
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "league": m["league"]["name"],
        "country": m["league"]["country"],
        "league_id": m["league"]["id"],
        "time": m["fixture"]["date"][11:16]
    }

    matches.append(match)

matches = matches[:30]

with open("data/matches_today.json","w") as f:
    json.dump(matches,f,indent=2)