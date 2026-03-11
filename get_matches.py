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

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

if "response" in data:
for m in data["response"]:

    match = {
        "fixture_id": m["fixture"]["id"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "league": m["league"]["name"],
        "home_id": m["teams"]["home"]["id"],
        "away_id": m["teams"]["away"]["id"],
        "time": m["fixture"]["date"]
    }

    matches.append(match)

with open("matches_today.json", "w") as f:
json.dump(matches, f, indent=4)

print("Partite trovate:", len(matches))