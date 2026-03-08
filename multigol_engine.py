import requests
import json
import os

API_KEY = os.getenv("37ddec86e8578a1ff3127d5c394da749")

headers = {
    "x-apisports-key": API_KEY
}

INPUT="data/matches_today.json"
OUTPUT="output/predictions.json"

with open(INPUT) as f:
    matches=json.load(f)

pred=[]

for m in matches:

    league=m["league_id"]
    season=m["season"]

    home_id=m["home_id"]
    away_id=m["away_id"]

    url="https://v3.football.api-sports.io/teams/statistics"

    home_stats=requests.get(
        url,
        headers=headers,
        params={"league":league,"season":season,"team":home_id}
    ).json()

    away_stats=requests.get(
        url,
        headers=headers,
        params={"league":league,"season":season,"team":away_id}
    ).json()

    try:

        hg=home_stats["response"]["goals"]["for"]["average"]["home"]
        ag=away_stats["response"]["goals"]["for"]["average"]["away"]

        hg=float(hg)
        ag=float(ag)

    except:
        continue

    expected=hg+ag

    if expected>2.5:
        ou="Over 2.5"
    else:
        ou="Under 2.5"

    if hg>1 and ag>1:
        btts="Yes"
    else:
        btts="No"

    if expected<2.3:
        mg="1-2"
    elif expected<2.8:
        mg="2-3"
    else:
        mg="2-4"

    pred.append({
        "home":m["home"],
        "away":m["away"],
        "over_under":ou,
        "btts":btts,
        "multigol":mg
    })

with open(OUTPUT,"w") as f:
    json.dump(pred[:10],f,indent=4)

print("predictions:",len(pred))
