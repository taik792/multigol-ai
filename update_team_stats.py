import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

# carica partite di oggi
with open("data/matches_today.json") as f:
    matches = json.load(f)

teams = {}

for m in matches:

    home = m["home"]
    away = m["away"]
    league = m.get("league_id")

    for team in [home, away]:

        if team in teams:
            continue

        try:
            url = f"https://v3.football.api-sports.io/teams/statistics?league={league}&season=2024&team={m['home_id'] if team==home else m['away_id']}"

            r = requests.get(url, headers=headers)
            data = r.json()

            stats = data["response"]

            played = stats["fixtures"]["played"]["total"]

            if played == 0:
                continue

            scored = stats["goals"]["for"]["total"]["total"] / played
            conceded = stats["goals"]["against"]["total"]["total"] / played

            teams[team] = {
                "scored": round(scored,2),
                "conceded": round(conceded,2)
            }

        except:
            continue


with open("data/teams_stats.json","w") as f:
    json.dump(teams,f)