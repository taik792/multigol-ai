import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

with open("matches.json") as f:
    matches = json.load(f)

teams = {}

for match in matches:

    for team_id in [match["home_id"], match["away_id"]]:

        if str(team_id) in teams:
            continue

        url = f"https://v3.football.api-sports.io/teams/statistics?team={team_id}&season=2024&league={match['league_id']}"

        r = requests.get(url, headers=headers).json()

        try:

            stats = r["response"]

            teams[str(team_id)] = {

                "scored_home": float(stats["goals"]["for"]["average"]["home"]),
                "scored_away": float(stats["goals"]["for"]["average"]["away"]),
                "conceded_home": float(stats["goals"]["against"]["average"]["home"]),
                "conceded_away": float(stats["goals"]["against"]["average"]["away"])

            }

        except:
            continue

with open("teams_stats.json","w") as f:
    json.dump(teams,f,indent=4)

print("Teams saved:",len(teams))