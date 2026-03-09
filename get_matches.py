import requests
import json
from datetime import datetime

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

today = datetime.now().strftime("%Y-%m-%d")

fixtures_url = "https://v3.football.api-sports.io/fixtures"

params = {
    "date": today,
    "timezone": "Europe/Rome"
}

response = requests.get(fixtures_url, headers=headers, params=params).json()

matches = []

for match in response["response"]:

    if match["fixture"]["status"]["short"] not in ["NS","TBD"]:
        continue

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_id = match["teams"]["home"]["id"]
    away_id = match["teams"]["away"]["id"]

    league_id = match["league"]["id"]
    season = match["league"]["season"]

    stats_url = "https://v3.football.api-sports.io/teams/statistics"

    home_stats = requests.get(
        stats_url,
        headers=headers,
        params={
            "team": home_id,
            "league": league_id,
            "season": season
        }
    ).json()

    away_stats = requests.get(
        stats_url,
        headers=headers,
        params={
            "team": away_id,
            "league": league_id,
            "season": season
        }
    ).json()

    try:

        home_attack = float(home_stats["response"]["goals"]["for"]["average"]["total"])
        home_def = float(home_stats["response"]["goals"]["against"]["average"]["total"])

        away_attack = float(away_stats["response"]["goals"]["for"]["average"]["total"])
        away_def = float(away_stats["response"]["goals"]["against"]["average"]["total"])

    except:

        home_attack = 1.5
        home_def = 1.3
        away_attack = 1.4
        away_def = 1.4

    # forma ultime 5 partite
    form_home = home_stats["response"]["form"]
    form_away = away_stats["response"]["form"]

    home_form_score = form_home.count("W")*3 + form_home.count("D")
    away_form_score = form_away.count("W")*3 + form_away.count("D")

    matches.append({

        "home": home,
        "away": away,

        "home_attack": home_attack,
        "home_def": home_def,

        "away_attack": away_attack,
        "away_def": away_def,

        "home_form": home_form_score,
        "away_form": away_form_score
    })

with open("matches.json","w",encoding="utf-8") as f:
    json.dump(matches,f,indent=4,ensure_ascii=False)

print("Partite salvate:",len(matches))
