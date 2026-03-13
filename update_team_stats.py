import requests
import json
import os
import time

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

# carichiamo le partite
with open("data/matches.json") as f:
    matches = json.load(f)

teams = set()

# prendiamo solo le prime 20 partite per limitare API
for m in matches[:20]:

    home_id = m["home_id"]
    away_id = m["away_id"]

    teams.add(home_id)
    teams.add(away_id)

stats = {}

for team_id in teams:

    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "team": team_id,
        "last": 10
    }

    try:

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

        # se non troviamo partite usiamo valori medi
        if games == 0:

            stats[team_id] = {
                "scored": 1.2,
                "conceded": 1.2
            }

        else:

            stats[team_id] = {
                "scored": goals_for / games,
                "conceded": goals_against / games
            }

        time.sleep(0.25)

    except:

        stats[team_id] = {
            "scored": 1.2,
            "conceded": 1.2
        }

# salviamo statistiche
with open("data/team_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("Statistiche squadre aggiornate:", len(stats))