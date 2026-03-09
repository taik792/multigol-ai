import json
import requests

API_KEY="37ddec86e8578a1ff3127d5c394da749"

headers={
"x-apisports-key":API_KEY
}

with open("matches.json","r",encoding="utf-8") as f:
    matches=json.load(f)

predictions=[]

for match in matches:

    home=match["home"]
    away=match["away"]

    league=match["league_id"]
    season=match["season"]

    home_id=match["home_id"]
    away_id=match["away_id"]

    date=match.get("date","")

    # statistiche casa
    url1=f"https://v3.football.api-sports.io/teams/statistics?league={league}&season={season}&team={home_id}"
    r1=requests.get(url1,headers=headers).json()

    # statistiche ospite
    url2=f"https://v3.football.api-sports.io/teams/statistics?league={league}&season={season}&team={away_id}"
    r2=requests.get(url2,headers=headers).json()

    h=r1["response"]
    a=r2["response"]

    home_goals=float(h["goals"]["for"]["average"]["total"])
    home_conceded=float(h["goals"]["against"]["average"]["total"])

    away_goals=float(a["goals"]["for"]["average"]["total"])
    away_conceded=float(a["goals"]["against"]["average"]["total"])

    # expected goals
    home_xg=(home_goals+away_conceded)/2
    away_xg=(away_goals+home_conceded)/2

    total=home_xg+away_xg

    # probabilità
    over_prob=min(95,round(total/4*100))
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

    score=over_prob+btts_prob

    predictions.append({

        "home":home,
        "away":away,
        "date":date,

        "multigol_home":home_range,
        "multigol_away":away_range,

        "over25_prob":over_prob,
        "btts_prob":btts_prob,

        "score":score

    })

# ordina per punteggio
predictions.sort(key=lambda x:x["score"],reverse=True)

# prendi solo 10 migliori
top10=predictions[:10]

# rimuovi score dal json finale
for p in top10:
    del p["score"]

with open("predictions.json","w",encoding="utf-8") as f:
    json.dump(top10,f,indent=4,ensure_ascii=False)

print("Top matches created:",len(top10))
