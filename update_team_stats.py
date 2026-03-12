import requests
import json

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

with open("matches.json") as f:
    matches = json.load(f)

try:
    with open("teams_stats.json") as f:
        stats = json.load(f)
except:
    stats = {}

for m in matches:

    for team in [m["home"], m["away"]]:

        if team in stats:
            continue

        url = "https://v3.football.api-sports.io/teams"
        params = {"search": team}

        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        if not data["response"]:
            continue

        team_id = data["response"][0]["team"]["id"]

        url = "https://v3.football.api-sports.io/teams/statistics"
        params = {
            "team": team_id,
            "league": 39,
            "season": 2024
        }

        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        if not data["response"]:
            continue

        g = data["response"]["goals"]

        scored = g["for"]["average"]["total"]
        conceded = g["against"]["average"]["total"]

        stats[team] = {
            "scored": float(scored),
            "conceded": float(conceded)
        }

        print("Stats salvate:", team)

with open("teams_stats.json", "w") as f:
    json.dump(stats, f, indent=2)