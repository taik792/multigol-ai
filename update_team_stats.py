import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches_today.json") as f:
    matches = json.load(f)

team_stats = {}

for m in matches:
    for team in [m["home"], m["away"]]:
        if team in team_stats:
            continue

        url = "https://v3.football.api-sports.io/teams/statistics"

        params = {
            "league": 39,  # placeholder (puoi migliorare dopo)
            "season": 2024,
            "team": team
        }

        try:
            r = requests.get(url, headers=headers, params=params).json()
            stats = r["response"]

            team_stats[team] = {
                "scored": stats["goals"]["for"]["average"]["total"],
                "conceded": stats["goals"]["against"]["average"]["total"]
            }
        except:
            team_stats[team] = {
                "scored": 1.2,
                "conceded": 1.2
            }

with open("data/team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=2)

print("Statistiche aggiornate")