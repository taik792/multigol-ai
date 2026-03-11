import json
import math

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/teams_stats.json") as f:
    stats = json.load(f)

predictions = []

league_avg_goals = 2.6

def poisson(lmbda,k):
    return (lmbda**k * math.exp(-lmbda))/math.factorial(k)

for m in matches:

    home = m["home"]
    away = m["away"]

    if home not in stats or away not in stats:
        continue

    home_scored = stats[home]["scored"]
    home_conceded = stats[home]["conceded"]

    away_scored = stats[away]["scored"]
    away_conceded = stats[away]["conceded"]

    home_attack = home_scored / 1.3
    home_defense = home_conceded / 1.3

    away_attack = away_scored / 1.3
    away_defense = away_conceded / 1.3

    home_xg = home_attack * away_defense * league_avg_goals/2
    away_xg = away_attack * home_defense * league_avg_goals/2

    home_probs = [poisson(home_xg,i) for i in range(7)]
    away_probs = [poisson(away_xg,i) for i in range(7)]

    matrix = {}

    for i in range(7):
        for j in range(7):
            matrix[(i,j)] = home_probs[i]*away_probs[j]

    over25 = sum(p for (i,j),p in matrix.items() if i+j>=3)
    btts = sum(p for (i,j),p in matrix.items() if i>0 and j>0)
    multigol = sum(p for (i,j),p in matrix.items() if 1<=i+j<=3)

    prob = int(multigol*100)

    if prob < 55:
        continue

    predictions.append({
        "home":home,
        "away":away,
        "league":m["league"],
        "country":m["country"],
        "time":m["time"],

        "combo":"Casa o Over 1.5",

        "multigol_home":"1-3",
        "multigol_away":"1-3",

        "over25":f"{int(over25*100)}%",
        "btts":f"{int(btts*100)}%",

        "probability":prob
    })

predictions = sorted(predictions,key=lambda x:x["probability"],reverse=True)[:30]

with open("data/predictions.json","w") as f:
    json.dump(predictions,f)