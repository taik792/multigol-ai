import requests
import json
import os

API_KEY = os.getenv("API_KEY")

headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/teams/statistics"

with open("data/matches_today.json") as f:
    matches = json.load(f)

team_stats = {}

for match in matches[:120]:

    league_id = match["league_id"]
    home_id = match["home_id"]
    away_id = match["away_id"]

    for team_id in [home_id, away_id]:

        if str(team_id) in team_stats:
            continue

        params = {
            "league": league_id,
            "season": 2024,
            "team": team_id
        }

        try:

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if "response" not in data:
                continue

            stats = data["response"]

            if not stats:
                continue

            goals_for = stats["goals"]["for"]["average"]["total"]
            goals_against = stats["goals"]["against"]["average"]["total"]

            team_stats[str(team_id)] = {
                "goals_for": goals_for,
                "goals_against": goals_against
            }

        except Exception as e:
            print("Errore squadra:", team_id)

print("Statistiche squadre aggiornate:", len(team_stats))

os.makedirs("data", exist_ok=True)

with open("data/team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=2)
