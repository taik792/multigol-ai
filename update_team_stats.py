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

for m in matches[:40]:

    home_id = m["home_id"]
    away_id = m["away_id"]
    league_id = m["league_id"]

    for team_id in [home_id, away_id]:

        team_id = str(team_id)

        if team_id in stats:
            continue

        url = "https://v3.football.api-sports.io/teams/statistics"

        params = {
            "team": team_id,
            "league": league_id,
            "season": 2025
        }

        r = requests.get(url, headers=headers, params=params)

        data = r.json()

        try:

            games = data["response"]["fixtures"]["played"]["total"]

            scored = data["response"]["goals"]["for"]["total"]["total"]
            conceded = data["response"]["goals"]["against"]["total"]["total"]

            if games == 0:
                continue

            stats[team_id] = {
                "scored": scored / games,
                "conceded": conceded / games
            }

        except:
            continue

os.makedirs("data", exist_ok=True)

with open("data/team_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("Statistiche squadre aggiornate:", len(stats))