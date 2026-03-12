import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

# carica partite
with open("data/matches.json") as f:
    matches = json.load(f)

teams = {}

for m in matches:
    teams[m["home"]] = m["home_id"]
    teams[m["away"]] = m["away_id"]

stats = {}

for team, team_id in teams.items():

    url = "https://v3.football.api-sports.io/teams/statistics"

    params = {
        "team": team_id,
        "league": 39,
        "season": 2024
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        continue

    data = r.json()

    if not data["response"]:
        continue

    d = data["response"]

    goals_for = d["goals"]["for"]["total"]["total"]
    goals_against = d["goals"]["against"]["total"]["total"]
    games = d["fixtures"]["played"]["total"]

    if games == 0:
        continue

    stats[team] = {
        "goals_for": goals_for / games,
        "goals_against": goals_against / games
    }

print("Statistiche squadre aggiornate:", len(stats))

with open("data/team_stats.json","w") as f:
    json.dump(stats,f,indent=4)