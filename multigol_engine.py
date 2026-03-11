import json
import math

def poisson(lmbda, k):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

with open("data/matches_today.json") as f:
    matches = json.load(f)

with open("data/teams_stats.json") as f:
    stats = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]
    league = m["league"]
    time = m["time"]

    if home not in stats or away not in stats:
        continue

    home_scored = stats[home]["scored"]
    home_conceded = stats[home]["conceded"]

    away_scored = stats[away]["scored"]
    away_conceded = stats[away]["conceded"]

    exp_home = (home_scored + away_conceded) / 2
    exp_away = (away_scored + home_conceded) / 2

    # probabilità gol
    home_goals = [poisson(exp_home,i) for i in range(6)]
    away_goals = [poisson(exp_away,i) for i in range(6)]

    # probabilità over 2.5
    over25 = 0

    for h in range(6):
        for a in range(6):
            if h+a >=3:
                over25 += home_goals[h]*away_goals[a]

    # probabilità BTTS
    btts = 0

    for h in range(1,6):
        for a in range(1,6):
            btts += home_goals[h]*away_goals[a]

    probability = int((over25 + btts)/2 *100)

    if probability < 55:
        continue

    prediction = {
        "home":home,
        "away":away,
        "league":league,
        "time":time,
        "combo":"Casa o Over 1.5",
        "multigol_home":"1-3",
        "multigol_away":"0-2",
        "over25":f"{int(over25*100)}%",
        "btts":f"{int(btts*100)}%",
        "probability":probability
    }

    predictions.append(prediction)

predictions = sorted(predictions, key=lambda x:x["probability"], reverse=True)

predictions = predictions[:30]

with open("data/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Pronostici creati:",len(predictions))
