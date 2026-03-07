import json
import os

with open("data/matches_today.json") as f:
    matches = json.load(f)

predictions = []

for m in matches:

    home = m["home"]
    away = m["away"]

    home_avg = m["home_goals_avg"]
    away_avg = m["away_goals_avg"]

    home_con = m["home_conceded"]
    away_con = m["away_conceded"]

    # stima gol attesi
    xg = (home_avg + away_avg + home_con + away_con) / 2

    if xg >= 2.3:

        prediction = {
            "match": f"{home} vs {away}",
            "expected_goals": round(xg,2),
            "multigol": "2-4",
            "confidence": int(xg * 30)
        }

        predictions.append(prediction)

os.makedirs("output", exist_ok=True)

with open("output/multigol_predictions.json","w") as f:
    json.dump(predictions,f,indent=4)

print("Multigol Engine completato")
