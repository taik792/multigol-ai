import json
import random

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    home_avg = random.uniform(0.8,2.2)
    away_avg = random.uniform(0.6,1.8)

    total = home_avg + away_avg

    if total >= 3:
        multigol = "2-4"
    elif total >= 2:
        multigol = "2-3"
    else:
        multigol = "1-3"

    if home_avg >= 1.8:
        home_goals = "1-3"
    elif home_avg >= 1.2:
        home_goals = "1-2"
    else:
        home_goals = "0-1"

    if away_avg >= 1.5:
        away_goals = "1-2"
    elif away_avg >= 1:
        away_goals = "0-2"
    else:
        away_goals = "0-1"

    confidence = round(random.uniform(70,90),1)

    predictions.append({
        "home":home,
        "away":away,
        "multigol":multigol,
        "home_goals":home_goals,
        "away_goals":away_goals,
        "confidence":confidence
    })

with open("output/predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Pronostici creati:",len(predictions))
