import json
import math

# carica partite
with open("data/matches_today.json", "r") as f:
    matches = json.load(f)

# carica statistiche squadre
with open("data/teams_stats.json", "r") as f:
    stats = json.load(f)

predictions = []

def poisson(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

for m in matches:

    home = m["home"]
    away = m["away"]

    if home not in stats or away not in stats:
        continue

    home_scored = stats[home]["scored"]
    home_conceded = stats[home]["conceded"]

    away_scored = stats[away]["scored"]
    away_conceded = stats[away]["conceded"]

    # gol attesi
    home_xg = (home_scored + away_conceded) / 2
    away_xg = (away_scored + home_conceded) / 2

    # probabilità gol
    home_probs = [poisson(home_xg, i) for i in range(6)]
    away_probs = [poisson(away_xg, i) for i in range(6)]

    total_probs = {}

    for i in range(6):
        for j in range(6):
            total_probs[(i, j)] = home_probs[i] * away_probs[j]

    # OVER 2.5
    over25 = sum(p for (i,j),p in total_probs.items() if i+j >=3)

    # BTTS
    btts = sum(p for (i,j),p in total_probs.items() if i>0 and j>0)

    # MULTIGOL 1-3
    multigol13 = sum(p for (i,j),p in total_probs.items() if 1 <= i+j <=3)

    prob = int(multigol13 * 100)

    if prob < 55:
        continue

    prediction = {
        "home": home,
        "away": away,
        "league": m["league"],
        "country": m["country"],
        "time": m["time"],

        "combo": "Casa o Over 1.5",

        "multigol_home": "1-3",
        "multigol_away": "1-3",

        "over25": f"{int(over25*100)}%",
        "btts": f"{int(btts*100)}%",

        "probability": prob
    }

    predictions.append(prediction)

# massimo 30 partite
predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:30]

with open("data/predictions.json", "w") as f:
    json.dump(predictions, f)