import json
import os

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]
    league = m["league"]

    home_avg = m["home_goals_avg"]
    away_avg = m["away_goals_avg"]

    home_con = m["home_conceded"]
    away_con = m["away_conceded"]

    xg = (home_avg + away_avg + home_con + away_con) / 2

    if xg < 1.5:
        multigol = "0-2"
    elif xg < 2.5:
        multigol = "1-3"
    elif xg < 3.5:
        multigol = "2-4"
    else:
        multigol = "2-5"

    prediction = {
        "match": f"{home} vs {away}",
        "league": league,
        "expected_goals": round(xg,2),
        "multigol": multigol,
        "confidence": int(xg * 30)
    }

    predictions.append(prediction)

os.makedirs("output", exist_ok=True)

with open("output/multigol_predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Multigol Engine completato")
