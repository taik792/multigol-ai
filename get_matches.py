import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/fixtures"

params = {
    "next": 30
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

matches = []

for game in data["response"]:

    match = {

        "home": game["teams"]["home"]["name"],
        "away": game["teams"]["away"]["name"],
        "home_id": game["teams"]["home"]["id"],
        "away_id": game["teams"]["away"]["id"],
        "league": game["league"]["name"],
        "league_id": game["league"]["id"],
        "time": game["fixture"]["date"][11:16]

    }

    matches.append(match)

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)

print("Matches saved:",len(matches))