import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "next": 50
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

matches = []

for game in data["response"]:

    fixture = game["fixture"]
    teams = game["teams"]
    league = game["league"]

    match = {

        "home": teams["home"]["name"],
        "away": teams["away"]["name"],
        "home_id": teams["home"]["id"],
        "away_id": teams["away"]["id"],
        "league": league["name"],
        "league_id": league["id"],
        "time": fixture["date"][11:16]

    }

    matches.append(match)

with open("matches.json", "w") as f:
    json.dump(matches, f, indent=4)

print("Matches saved:", len(matches))