import requests
import json
from datetime import datetime, timedelta

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

matches = []

dates = [
    datetime.now().strftime("%Y-%m-%d"),
    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
]

for date in dates:

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": date,
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for game in data["response"]:

        match = {
            "date": game["fixture"]["date"],
            "league": game["league"]["name"],
            "home": game["teams"]["home"]["name"],
            "away": game["teams"]["away"]["name"],
            "fixture_id": game["fixture"]["id"]
        }

        matches.append(match)

with open("data/matches_today.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Partite trovate:", len(matches))
