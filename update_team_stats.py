import json
import requests

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches_today.json") as f:
    matches = json.load(f)

try:
    with open("data/teams_stats.json") as f:
        stats = json.load(f)
except:
    stats = {}

for m in matches:

    home = m["home"]
    away = m["away"]
    league = m["league"]

    teams = [home, away]

    for team in teams:

        if team in stats:
            continue

        url = "https://v3.football.api-sports.io/teams/statistics"

        params = {
            "league": m["league_id"],
            "season": 2024,
            "team": m["home_id"] if team == home else m["away_id"]
        }

        r = requests.get(url, headers=headers, params=params).json()

        try:

            scored = r["response"]["goals"]["for"]["average"]["total"]
            conceded = r["response"]["goals"]["against"]["average"]["total"]

            stats[team] = {
                "scored": float(scored),
                "conceded": float(conceded)
            }

        except:
            continue

with open("data/teams_stats.json","w") as f:
    json.dump(stats,f,indent=4)

print("Statistiche aggiornate:",len(stats))