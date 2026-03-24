import requests
import json
import os
import time

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

stats = {}

for m in matches:
    for team_id in [m["home_id"], m["away_id"]]:

        key = f"{team_id}_{m['league_id']}"

        if key in stats:
            continue

        url = f"https://v3.football.api-sports.io/teams/statistics?team={team_id}&league={m['league_id']}&season={m['season']}"

        res = requests.get(url, headers=headers).json()

        try:
            data = res["response"]

            stats[key] = {
                "team_id": team_id,
                "goals_for": data["goals"]["for"]["average"]["total"],
                "goals_against": data["goals"]["against"]["average"]["total"]
            }

            print(f"OK stats team {team_id}")

        except:
            print(f"Errore stats team {team_id}")

        time.sleep(1.2)  # evita ban API

with open("data/team_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("Stats salvate")