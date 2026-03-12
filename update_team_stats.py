import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches.json") as f:
    matches = json.load(f)

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

        if not data:
            continue

        goals_for = 0
        goals_against = 0
        games = 0

        for f in data:

            home_id = f["teams"]["home"]["id"]
            away_id = f["teams"]["away"]["id"]

            home_goals = f["goals"]["home"]
            away_goals = f["goals"]["away"]

            if home_goals is None or away_goals is None:
                continue

            if home_id == team_id:
                goals_for += home_goals
                goals_against += away_goals
            else:
                goals_for += away_goals
                goals_against += home_goals

            games += 1

        if games == 0:
            continue

        stats[team_name] = {
            "goals_for": goals_for / games,
            "goals_against": goals_against / games
        }

print("Statistiche squadre aggiornate:", len(stats))

with open("data/team_stats.json","w") as f:
    json.dump(stats,f,indent=4)