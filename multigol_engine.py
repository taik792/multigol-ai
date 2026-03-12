import json
import math

with open("data/matches.json") as f:
    matches = json.load(f)

with open("data/team_stats.json") as f:
    stats = json.load(f)

predictions = []

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

for m in matches:

    home = m["home"]
    away = m["away"]

    if home not in stats or away not in stats:
        continue

    home_attack = stats[home]["goals_for"]
    home_def = stats[home]["goals_against"]

    away_attack = stats[away]["goals_for"]
    away_def = stats[away]["goals_against"]

    home_exp = (home_attack + away_def) / 2
    away_exp = (away_attack + home_def) / 2

    total_exp = home_exp + away_exp

    over25 = 1 - sum(poisson(total_exp, i) for i in range(3))
    btts = 1 - (poisson(home_exp,0) + poisson(away_exp,0) - poisson(home_exp,0)*poisson(away_exp,0))

    multigol = 0
    for i in range(1,5):
        multigol += poisson(total_exp, i)

    predictions.append({
        "home": home,
        "away": away,
        "league": m["league"],
        "over25": round(over25*100,1),
        "btts": round(btts*100,1),
        "multigol_1_4": round(multigol*100,1)
    })

print("Pronostici generati:", len(predictions))

with open("data/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)