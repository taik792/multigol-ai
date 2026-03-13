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

for match in matches[:40]:  # limitiamo per non consumare API

    league_id = match["league_id"]
    home_id = match["home_id"]
    away_id = match["away_id"]

    for team_id in [home_id, away_id]:

        if str(team_id) in team_stats:
            continue

        url = "https://v3.football.api-sports.io/teams/statistics"

        params = {
            "league": league_id,
            "season": 2025,
            "team": team_id
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data["response"]:
            stats = data["response"]

            team_stats[str(team_id)] = {
                "goals_for": stats["goals"]["for"]["total"]["average"],
                "goals_against": stats["goals"]["against"]["total"]["average"],
                "over25": stats["goals"]["for"]["total"]["total"],
                "btts": stats["both_teams_score"]["percentage"]
            }

print("Statistiche squadre aggiornate:", len(team_stats))

os.makedirs("data", exist_ok=True)

with open("data/team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=2)