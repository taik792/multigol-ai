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

teams = set()

# prendiamo solo le prime 20 partite (40 squadre max)
for m in matches[:20]:

    home = m.get("home_id")
    away = m.get("away_id")

    if home:
        teams.add(home)

    if away:
        teams.add(away)

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

        if home == team_id:
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

    time.sleep(0.25)

with open("data/team_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("Statistiche squadre aggiornate:", len(stats))