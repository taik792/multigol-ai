import requests
import json
import os
import time

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches.json") as f:
    matches = json.load(f)

# prendiamo solo le prime 40 partite
matches = matches[:40]

teams = {}

for m in matches:

    home_id = str(m["teams"]["home"]["id"])
    away_id = str(m["teams"]["away"]["id"])

    teams[home_id] = m["teams"]["home"]["name"]
    teams[away_id] = m["teams"]["away"]["name"]

stats = {}

for team_id in teams:

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "team": team_id,
        "last": 10
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    goals_for = 0
    goals_against = 0
    games = 0

    for f in data["response"]:

        home = f["teams"]["home"]["id"]

        if home == int(team_id):
            gf = f["goals"]["home"]
            ga = f["goals"]["away"]
        else:
            gf = f["goals"]["away"]
            ga = f["goals"]["home"]

        if gf is None or ga is None:
            continue

        goals_for += gf
        goals_against += ga
        games += 1

    if games > 0:

        stats[team_id] = {
            "scored": goals_for / games,
            "conceded": goals_against / games
        }

    time.sleep(0.3)

with open("data/team_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("Statistiche squadre aggiornate:", len(stats))