import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://v3.football.api-sports.io/teams/statistics"

headers = {
    "x-apisports-key": API_KEY
}

with open("data/matches_today.json") as f:
    matches = json.load(f)

# carica stats se esistono
if os.path.exists("data/team_stats.json"):
    with open("data/team_stats.json") as f:
        team_stats = json.load(f)
else:
    team_stats = {}

updated = 0

for match in matches:

    league_id = match["league_id"]

    for team_id in [match["home_id"], match["away_id"]]:

        team_id = str(team_id)

        # 🔥 BLOCCO API: se già esiste → NON CHIAMA API
        if team_id in team_stats:
            continue

        params = {
            "league": league_id,
            "season": 2024,
            "team": team_id
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if not data.get("response"):
                continue

            stats = data["response"]

            team_stats[team_id] = {
                "goals_for": stats["goals"]["for"]["average"]["total"],
                "goals_against": stats["goals"]["against"]["average"]["total"]
            }

            updated += 1

        except:
            print("Errore squadra:", team_id)

print("Statistiche nuove scaricate:", updated)

with open("data/team_stats.json", "w") as f:
    json.dump(team_stats, f, indent=2)