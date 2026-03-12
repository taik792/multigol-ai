import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches.json") as f:
    matches = json.load(f)

# prendiamo solo prime 20 partite
matches = matches[:20]

stats = {}

for m in matches:

    teams = [
        (m["home"], m["home_id"]),
        (m["away"], m["away_id"])
    ]

    for team_name, team_id in teams:

        if team_name in stats:
            continue

        url = "https://v3.football.api-sports.io/fixtures"

        params = {
            "team": team_id,
            "last": 10
        }

        r = requests.get(url, headers=headers, params=params)

        if r.status_code != 200:
            continue

        data = r.json()["response"]

        goals_for = 0
        goals_against = 0
        games = 0

        for f in data:

            home = f["teams"]["home"]["id"]
            away = f["teams"]["away"]["id"]

            hg = f["goals"]["home"]
            ag = f["goals"]["away"]

            if hg is None or ag is None:
                continue

            if home == team_id:
                goals_for += hg
                goals_against += ag
            else:
                goals_for += ag
                goals_against += hg

            games += 1

        if games == 0:
            continue

        stats[team_name] = {
            "goals_for": goals_for/games,
            "goals_against": goals_against/games
        }

print("Statistiche squadre aggiornate:", len(stats))

with open("data/team_stats.json","w") as f:
    json.dump(stats,f,indent=4)