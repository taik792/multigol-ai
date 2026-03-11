import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
 "x-apisports-key": API_KEY
}

with open("data/matches_today.json") as f:
 matches = json.load(f)

stats = {}

for m in matches:

 for team in [("home_id","home"),("away_id","away")]:

    team_id = m[team[0]]
    league_id = m["league_id"]

    url = "https://v3.football.api-sports.io/teams/statistics"

    params = {
     "team": team_id,
     "league": league_id,
     "season": 2024
    }

    r = requests.get(url,headers=headers,params=params).json()

    if r["response"]:

        data = r["response"]

        scored = data["goals"]["for"]["average"]["total"]
        conceded = data["goals"]["against"]["average"]["total"]

        stats[team_id] = {
          "scored": float(scored),
          "conceded": float(conceded)
        }

with open("data/teams_stats.json","w") as f:
 json.dump(stats,f,indent=2)