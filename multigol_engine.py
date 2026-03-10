import json
import math

def poisson(k,lam):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

with open("matches.json") as f:
    matches=json.load(f)

with open("teams_stats.json") as f:
    stats=json.load(f)

predictions=[]

for match in matches:

    home_id=str(match["home_id"])
    away_id=str(match["away_id"])

    if home_id not in stats or away_id not in stats:
        continue

    home=match["home"]
    away=match["away"]
    league=match["league"]
    time=match["time"]

    home_scored=stats[home_id]["scored_home"]
    home_conceded=stats[home_id]["conceded_home"]

    away_scored=stats[away_id]["scored_away"]
    away_conceded=stats[away_id]["conceded_away"]

    expected_home=(home_scored+away_conceded)/2
    expected_away=(away_scored+home_conceded)/2

    home_probs=[poisson(i,expected_home) for i in range(6)]
    away_probs=[poisson(i,expected_away) for i in range(6)]

    over25=0
    btts=0

    for h in range(6):
        for a in range(6):

            p=home_probs[h]*away_probs[a]

            if h+a>=3:
                over25+=p

            if h>=1 and a>=1:
                btts+=p

    probability=int(max(over25,btts)*100)

    predictions.append({

        "home":home,
        "away":away,
        "league":league,
        "time":time,
        "over25":"Yes" if over25>0.5 else "No",
        "btts":"Yes" if btts>0.5 else "No",
        "probability":probability

    })

with open("predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Predictions:",len(predictions))