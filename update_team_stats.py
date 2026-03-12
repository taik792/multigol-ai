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

teams = set()

for m in matches:
    teams.add(m["home"])
    teams.add(m["away"])

stats = {}

for team in teams:

    url = "https://v3.football.api-sports.io/teams"

    params = {
        "search": team
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        continue

    data = r.json()

    if not data["response"]:
        continue

    team_id = data["response"][0]["team"]["id"]

    url_stats = "https://v3.football.api-sports.io/teams/statistics"

    params_stats = {
        "team": team_id,
        "league": 39,
        "season": 2024
    }

    r2 = requests.get(url_stats, headers=headers, params=params_stats)

    if r2.status_code != 200:
        continue

    data2 = r2.json()

    if not data2["response"]:
        continue

    d = data2["response"]

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