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

r = requests.get(url, headers=headers, params=params)

data = r.json()

matches = []

now = datetime.utcnow()

for m in data["response"]:

    match_time = datetime.strptime(m["fixture"]["date"][:19], "%Y-%m-%dT%H:%M:%S")

    # mostra partite 1 ora prima
    if match_time < now - timedelta(hours=1):
        continue

    matches.append({

        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],

        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],

        "league": m["league"]["name"],
        "league_id": m["league"]["id"],

        "country": m["league"]["country"],

        "time": match_time.strftime("%H:%M")

    })

with open("data/matches_today.json","w") as f:
    json.dump(matches,f)