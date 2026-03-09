import json
import requests

API_KEY = "37ddec86e8578a1ff3127d5c394da749"

headers = {
    "x-apisports-key": API_KEY
}

with open("matches.json","r",encoding="utf-8") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]
    league=match.get("league_id")
    season=match.get("season")

    # statistiche squadra casa
    url_home=f"https://v3.football.api-sports.io/teams/statistics?league={league}&season={season}&team={match['home_id']}"
    r1=requests.get(url_home,headers=headers).json()

    # statistiche squadra ospite
    url_away=f"https://v3.football.api-sports.io/teams/statistics?league={league}&season={season}&team={match['away_id']}"
    r2=requests.get(url_away,headers=headers).json()

    home_stats=r1["response"]
    away_stats=r2["response"]

    home_goals=home_stats["goals"]["for"]["average"]["total"]
    away_goals=away_stats["goals"]["for"]["average"]["total"]

    home_conceded=home_stats["goals"]["against"]["average"]["total"]
    away_conceded=away_stats["goals"]["against"]["average"]["total"]

    # expected goals stimato
    home_xg=(float(home_goals)+float(away_conceded))/2
    away_xg=(float(away_goals)+float(home_conceded))/2

    total=home_xg+away_xg

    # probabilità over
    over_prob=min(95,round(total/4*100))

    # probabilità btts
    btts_prob=min(90,round((home_xg*away_xg)/2*100))

    # multigol casa
    if home_xg<1:
        home_range="0-1"
    elif home_xg<2:
        home_range="1-2"
    else:
        home_range="1-3"

    # multigol ospite
    if away_xg<1:
        away_range="0-1"
    elif away_xg<2:
        away_range="1-2"
    else:
        away_range="1-3"

    predictions.append({

        "home":home,
        "away":away,
        "date":match.get("date",""),

        "multigol_home":home_range,
        "multigol_away":away_range,

        "over25_prob":over_prob,
        "btts_prob":btts_prob

    })

with open("predictions.json","w",encoding="utf-8") as f:
    json.dump(predictions,f,indent=4,ensure_ascii=False)

print("Predictions created:",len(predictions))
