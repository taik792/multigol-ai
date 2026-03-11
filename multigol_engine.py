import json
import math

with open("matches.json") as f:
    matches = json.load(f)

with open("teams_stats.json") as f:
    stats = json.load(f)

predictions = []

def poisson(lam,k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

for m in matches:

    home = m["home"]
    away = m["away"]

    # se mancano statistiche usa medie calcio
    home_stats = stats.get(home,{"scored":1.5,"conceded":1.3})
    away_stats = stats.get(away,{"scored":1.5,"conceded":1.3})

    home_xg = (home_stats["scored"] + away_stats["conceded"]) / 2
    away_xg = (away_stats["scored"] + home_stats["conceded"]) / 2

    over25 = 0
    btts = 0

    for h in range(6):
        for a in range(6):

            p = poisson(home_xg,h) * poisson(away_xg,a)

            if h+a >=3:
                over25 += p

            if h>0 and a>0:
                btts += p

    over25 = round(over25*100)
    btts = round(btts*100)

    probability = round((over25+btts)/2)

    if over25 < 50:
        continue

    if btts < 45:
        continue

    predictions.append({

        "home":home,
        "away":away,
        "league":m["league"],
        "country":m["country"],
        "time":m["time"],

        "over25":over25,
        "btts":btts,
        "probability":probability

    })

with open("predictions.json","w") as f:
    json.dump(predictions,f,indent=2)