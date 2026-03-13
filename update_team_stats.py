import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

# carica partite trovate
with open("data/matches_today.json") as f:
    matches = json.load(f)

team_stats = {}

# limitiamo per non consumare API
for match in matches[:20]:

    league_id = match["league_id"]
    home_id = match["home_id"]
    away_id = match["away_id"]

    for team_id in [home_id, away_id]:

        if str(team_id) in team_stats:
            continue

        url = "https://v3.football.api-sports.io/teams/statistics"

        params = {
            "league": league_id,
            "season": 2023,
            "team": team_id
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if not data.get("response"):
                continue

            stats = data["response"]

            goals_for = stats["goals"]["for"]["average"]["total"]
            goals_against = stats["goals"]["against"]["average"]["total"]
            btts = stats["both_teams_score"]["percentage"]

            team_stats[str(team_id)] = {
                "goals_for": goals_for,
                "goals_against": goals_against,
                "btts": btts
            }

        except:
            continue

print("Statistiche squadre aggiornate:", len(team_stats))

os.makedirs("data", exist_ok=True)

with open("data/team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=2)
