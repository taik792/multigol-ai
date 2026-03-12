import requests
import json
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/fixtures"

today = datetime.utcnow().strftime("%Y-%m-%d")
tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")

matches = []

def get_games(date):

    params = {
        "date": date
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    if "response" not in data:
        return []

    games = []

    for m in data["response"]:

        if m["fixture"]["status"]["short"] == "NS":

            games.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "league": m["league"]["name"],
                "time": m["fixture"]["date"]
            })

    return games


matches += get_games(today)
matches += get_games(tomorrow)

with open("matches.json","w") as f:
    json.dump(matches,f,indent=4)

print("Partite trovate:",len(matches))