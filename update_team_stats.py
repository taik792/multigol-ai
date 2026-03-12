import requests
import json
import os

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

headers = {
    "x-apisports-key": API_KEY
}

# carica partite
with open("matches.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

teams = set()

for m in matches:
    teams.add(m["home"])
    teams.add(m["away"])

stats = {}

for team in teams:
    try:
        url = "https://v3.football.api-sports.io/teams"
        r = requests.get(url, headers=headers, params={"search": team})
        data = r.json()

        team_id = data["response"][0]["team"]["id"]

        url = "https://v3.football.api-sports.io/fixtures"
        r = requests.get(url, headers=headers, params={
            "team": team_id,
            "last": 10
        })

        fixtures = r.json()["response"]

        goals_for = 0
        goals_against = 0
        games = 0

        for f in fixtures:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]

            gh = f["goals"]["home"]
            ga = f["goals"]["away"]

            if gh is None or ga is None:
                continue

            if home == team:
                goals_for += gh
                goals_against += ga
            else:
                goals_for += ga
                goals_against += gh

            games += 1

        if games > 0:
            stats[team] = {
                "scored": round(goals_for / games, 2),
                "conceded": round(goals_against / games, 2)
            }

    except:
        continue

with open("teams_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)

print("Statistiche squadre aggiornate:", len(stats))